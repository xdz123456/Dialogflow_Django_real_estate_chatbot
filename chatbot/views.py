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
from django.utils import timezone

current_property = [None, None, None, None, None, None]
current_user = None


def index(request):
    global current_user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                current_user = user
                return redirect(reverse('chatbot:chatform'))
            else:
                return render(request, 'chatbot/logerror.html')
        else:
            return render(request, 'chatbot/logerror.html')
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
    global current_user
    current_user = None
    logout(request)
    return redirect(reverse('chatbot:index'))


def deal_with_intent(intent_name, para):
    global current_property
    if intent_name == "Sell":
        current_property = [None, None, None, None, None, None]
    if intent_name == "City":
        current_property[0] = para
    if intent_name == "Address":
        current_property[1] = para
    if intent_name == "Postcode":
        current_property[2] = para
    if intent_name == "Type":
        current_property[3] = para
    if intent_name == "BedroomNum":
        current_property[4] = para
    if intent_name == "Price":
        current_property[5] = para
    if intent_name == "ConfirmTrue":
        my_property = Property()
        my_property.property_city = current_property[0]
        my_property.property_address = current_property[1]
        my_property.property_postcode = current_property[2]
        my_property.property_type = current_property[3]
        my_property.property_num_bedroom = int(current_property[4])
        my_property.property_price = float(current_property[5])
        my_property.property_date = timezone.now()
        my_property.save()
        my_property.property_belong.add(current_user)
        print("Save successfully")


@login_required
def chat(request):
    output_text = " "
    intent_name = None
    my_parameter = None
    form = InputTextForm()
    if request.method == 'POST':
        form = InputTextForm(request.POST)

    if form.is_valid():
        chat_data = form.cleaned_data['input_text']
        form.save(commit=True)
        intent_name, my_parameter, output_text = chat_with_me(chat_data)
        form = InputTextForm()
    else:
        print(form.errors)

    deal_with_intent(intent_name, my_parameter)

    print(current_property)

    context_dict = {'output_text': output_text, 'form': form}
    return render(request, 'chatbot/chatform.html', context=context_dict)
