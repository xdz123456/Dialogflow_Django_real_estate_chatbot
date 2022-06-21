from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'boldmessage': 'Welcome to ChatBot'}
    return render(request, 'chatbot/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': '2663048X'}
    return render(request, 'chatbot/about.html', context=context_dict)
# Create your views here.
