from django.shortcuts import render
from chatbot.forms import InputTextForm
from chatbot.forms import UserForm
from chatbot.realestatechatbot import chat_with_me
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from chatbot.models import Property

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('chatbot:chatform'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'chatbot/index.html')


def about(request):
    context_dict = {'boldmessage': '2663048X'}
    return render(request, 'chatbot/about.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'chatbot/register.html', context={'user_form': user_form, 'registered': registered})

def user_logout(request):
    logout(request)
    return redirect(reverse('chatbot:index:index'))

@login_required
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

    context_dict = {'output_text': output_text, 'form': form}
    return render(request, 'chatbot/chatform.html', context=context_dict)
