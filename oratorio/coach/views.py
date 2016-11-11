from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.conf import settings
from .settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from tempfile import TemporaryFile
import speech_recognition as sr

def upload(request):
    if request.method == 'POST':
        # create a temp file to store the blob
        tempfile = TemporaryFile()
        tempfile.write(request.body)
        file = File(tempfile)
        # save the file
        fs = FileSystemStorage()
        filename = fs.save("testfile.wav", file)
        uploaded_file_url = MEDIA_ROOT + "/" + filename
        tempfile.close()
        
        # testing using google speech-to-text
        test_with_google = True;
        if test_with_google:
            r = sr.Recognizer()
            # feed file to speech-to-text APIs
            # tested with Google Speech Recognition here
            try:
                with sr.AudioFile(uploaded_file_url) as source:
                    audio = r.record(source)
                print("You said: " + r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return redirect('result')
    return redirect('index')

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
