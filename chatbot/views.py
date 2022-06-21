from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'boldmessage': 'Welcome to ChatBot'}
    return render(request, 'chatbot/index.html', context=context_dict)


def about(request):
    return HttpResponse("<a href='/chatbot/'>Back</a>")
# Create your views here.
