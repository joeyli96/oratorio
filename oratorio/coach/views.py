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
from .utils import verify_id_token

# This class contains view functions that take a Web request
# and returns a Web response. This can be the HTML contents
# of a Web page, error, etc.

def login(request):
    if request.method != 'POST':
        return redirect('index')

    token = request.COOKIES['id_token']
    idinfo = verify_id_token(token)
    if not idinfo:
        return HttpResponseBadRequest()

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
        idinfo = verify_id_token(token)
        if not idinfo:
            return HttpResponseBadRequest()
        users = User.objects.filter(email=idinfo['email'])
        if users:
             user=users[0]
    except KeyError:
        user = User(name="temp", email="temp")
        user.save()
    # create speech and recording
    num_speeches = len(Speech.objects.filter(user=user))
    speech_name = "speech" + str(num_speeches + 1)
    speech = Speech(user=user, name=speech_name)
    speech.save()
    recording = Analyzer.create_recording(
        audio_dir=uploaded_file_url, speech=speech)
    recording.save()
    print json.dumps(recording.transcript)
    # send transcript and pace to result page
    template = loader.get_template('coach/results.html')
    context = {
        'transcript': recording.get_transcript_text(),
        'pace': recording.get_avg_pace(),
    }
    return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('coach/index.html')

    try:
        token = request.COOKIES['id_token']
    except KeyError:
        return HttpResponse(template.render({}, request))


    idinfo = verify_id_token(token)
    if not idinfo:
        return HttpResponseBadRequest()

    recordings = []
    for speech in Speech.objects.filter(user__email=idinfo["email"]):
        for recording in Recording.objects.filter(speech=speech):
            recordings.append(recording)

    context = { 'recordings': recordings, }
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template('coach/profile.html')
    context = {}
    return HttpResponse(template.render(context, request))


def result(request):
    template = loader.get_template('coach/results.html')
    context = {}
    return HttpResponse(template.render(context, request))


def userdocs(request):
    template = loader.get_template('coach/userdocs.html')
    context = {}
    return HttpResponse(template.render(context, request))
