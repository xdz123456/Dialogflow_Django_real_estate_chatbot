from django.shortcuts import render
from django.http import HttpResponse
from chatbot.forms import InputTextForm
from django.shortcuts import redirect
from chatbot.realestatechatbot import chat_with_me

def index(request):
    context_dict = {'boldmessage': 'Welcome to ChatBot'}
    return render(request, 'chatbot/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': '2663048X'}
    return render(request, 'chatbot/about.html', context=context_dict)


def chat(request):
    output_text = " "

    form = InputTextForm()
    if request.method == 'POST':
        form = InputTextForm(request.POST)

    if form.is_valid():
        chat_data = form.cleaned_data['input_text']
        form.save(commit=True)
        output_text = chat_with_me(chat_data)
    else:
        print(form.errors)

    context_dict = {'output_text': output_text, 'form':form}
    return render(request, 'chatbot/chatform.html', context=context_dict)