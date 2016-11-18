from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from .settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from tempfile import TemporaryFile
from .models import User, Speech, Recording
from .analyzer import Analyzer
import json

# This class contains view functions that take a Web request
# and returns a Web response. This can be the HTML contents
# of a Web page, error, etc.


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
    # get user Joey
    # if Joey does not exist, create user
    users = User.objects.filter(name="Joey")
    if not users:
        user = User(name="Joey", email="joey@joey.com")
        user.save()
    else:
        user = users[0]
    # create speech and recording
    num_speeches = len(Speech.objects.all())
    speech_name = "speech" + str(num_speeches + 1)
    speech = Speech(user=user, name=speech_name)
    speech.save()
    recording = Analyzer.create_recording(
        audio_dir=uploaded_file_url, speech=speech)
    recording.save()
    print json.dumps(recording.transcript)
    # send transcript and pace to result page
    template = loader.get_template('coach/results.html')
    rec_len = recording.get_recording_length()
    if rec_len != 0:
        avg_pace = 60 * recording.get_word_count() / rec_len
    else:
        avg_pace = 0
    transcript_text = recording.get_transcript_text()

    most_frequent_words = Analyzer.get_word_frequency(transcript_text, 5)
    for word in most_frequent_words :
        print word[0]

    pause_list, pauses = Analyzer.get_pauses(recording.transcript)


    context = {
        'transcript': transcript_text,
        'pace': avg_pace,
        'most_frequent_words': most_frequent_words,
        'pauses': pauses
    }
    return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('coach/index.html')
    context = {}
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
