from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.conf import settings
from .models import Document
from .forms import DocumentForm

import speech_recognition as sr

def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        r = sr.Recognizer()
        if form.is_valid():
            file = request.FILES['document']
            # feed file to speech-to-text APIs
            # tested with Google Speech Recognition here
            try:
                with sr.AudioFile(file) as source:
                    audio = r.record(source)
                print("You said: " + r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return redirect('result')
    else:
        form = DocumentForm()
    return render(request, 'coach/model_form_upload.html', {
        'form': form
    })

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
