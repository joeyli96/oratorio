from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.conf import settings
from .settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from tempfile import TemporaryFile
from .models import User, Speech, Recording
from .analyzer import Analyzer
import json
import utils
from oauth2client import crypt

# This class contains view functions that take a Web request
# and returns a Web response. This can be the HTML contents
# of a Web page, error, etc.


def login(request):
    if request.method != 'POST':
        return redirect('index')

    token = request.COOKIES['id_token']
    try:
        idinfo = utils.verify_id_token(token)
    except crypt.AppIdentityError as e:
        return HttpResponseBadRequest(e)

    user = User.objects.filter(email=idinfo["email"])
    if not user:
        User(name=idinfo["name"], email=idinfo["email"]).save()

    return HttpResponse("OK")


def upload(request):
    if request.method != 'POST':
        return redirect('index')

    # create a temp file to store the blob
    tempfile = TemporaryFile()
    tempfile.write(request.body)
    file = File(tempfile)
    # save the file
    fs = FileSystemStorage()
    filename = fs.save("testfile.wav", file)
    uploaded_file_url = MEDIA_ROOT + "/" + filename
    tempfile.close()

    try:
        token = request.COOKIES['id_token']
        try:
            idinfo = utils.verify_id_token(token)
        except crypt.AppIdentityError as e:
            return HttpResponseBadRequest(e)
        users = User.objects.filter(email=idinfo['email'])
        if users:
            user = users[0]
    except KeyError:
        user = User(name="temp", email="temp")
        user.save()
    # create speech and recording
    num_speeches = len(Speech.objects.filter(user=user))
    speech_name = "speech" + str(num_speeches + 1)
    speech = Speech(name=speech_name, user=user)
    speech.save()
    try:
        recording = Recording.create(
            audio_dir=uploaded_file_url, speech=speech)
        recording.save()
    except Exception as e:
        # Delete empty speech if anything goes wrong
        speech.delete()
        return HttpResponseBadRequest(e)
    return HttpResponse(str(recording.id))


def index(request):
    template = loader.get_template('coach/index.html')

    try:
        token = request.COOKIES['id_token']
    except KeyError:
        return HttpResponse(template.render({}, request))
    try:
        context = utils.get_context(token)
    except crypt.AppIdentityError as e:
        return HttpResponseBadRequest(e)
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template('coach/profile.html')

    try:
        token = request.COOKIES['id_token']
        try:
            idinfo = utils.verify_id_token(token)
        except crypt.AppIdentityError as e:
            return HttpResponseBadRequest(e)
        users = User.objects.filter(email=idinfo['email'])
        if users:
            user = users[0]
        else:
            return redirect('index')
    except KeyError:
        return redirect('index')
    try:
        context = utils.get_context(token)
    except crypt.AppIdentityError as e:
        return HttpResponseBadRequest(e)
    context['user'] = user
    context['tones'] = user.get_avg_tone()
    return HttpResponse(template.render(context, request))


def result(request):
    # If there is no id_token, user is not logged in, so redirect to index
    try:
        token = request.COOKIES['id_token']
    except KeyError:
        return redirect('index')

    # If the id_token is invalid, return error
    try:
        idinfo = utils.verify_id_token(token)
    except crypt.AppIdentityError as e:
        return HttpResponseBadRequest(e)

    # If the user doesn't exist in the database, return error
    users = User.objects.filter(email=idinfo['email'])
    if users:
        user = users[0]
    else:
        return HttpResponseBadRequest("User does not exist: how did you get here?")

    # If no recording id was provided as url parameter, return error
    rec_id = request.GET.get('rid', '')
    if not rec_id:
        return HttpResponseBadRequest("No ID was provided")

    if rec_id == "-1":
        return HttpResponseBadRequest("An error has occurred")

    # Check that current user has access to the requested recording, and that
    # the recording exists. Otherwise return error.
    valid_recs = Recording.objects.filter(speech__user=user, id=rec_id)
    if not valid_recs:
        return HttpResponseBadRequest("Permission denied: how did you get here?")
    rec = valid_recs[0]

    # Populate context with sidebar data, transcript text and avg pace
    try:
        context = utils.get_context(token)
    except crypt.AppIdentityError as e:
        return HttpResponseBadRequest(e)
    context['transcript'] = rec.get_transcript_text()
    context['pace'] = rec.get_avg_pace()
    context['pauses'] = rec.pauses

    most_frequent_words = Analyzer.get_word_frequency(rec.get_transcript_text(), 5)

    context['most_frequent_words'] = most_frequent_words
    context['recording'] = rec

    template = loader.get_template('coach/results.html')
    return HttpResponse(template.render(context, request))


def userdocs(request):
    template = loader.get_template('coach/userdocs.html')
    try:
        token = request.COOKIES['id_token']
    except KeyError:
        return HttpResponse(template.render({}, request))
    try:
        context = utils.get_context(token)
    except crypt.AppIdentityError as e:
        return HttpResponseBadRequest(e)
    return HttpResponse(template.render(context, request))
