from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# This class contains view functions that take a Web request
# and returns a Web response. This can be the HTML contents
# of a Web page, error, etc.


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
