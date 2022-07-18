from django.shortcuts import render
from chatbot.forms import InputTextForm
from chatbot.forms import UserForm
from chatbot.realestatechatbot import chat_with_me
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from chatbot.models import Property
from django.utils import timezone

# Set up the global value
# current_property is the Property class which is waiting for storing in the database
# current_user is User which is logged in
current_property = [None, None, None, None, None, None]
current_query = [None, None, None, None, None, None]
current_user = None


# The index page's view function which provide a login function
def index(request):
    # Set the current_user as the global value
    global current_user
    # Do the auth using form from frontend
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # Login to the system
        if user:
            if user.is_active:
                login(request, user)
                current_user = user
                # redirect to the chatform page
                return redirect(reverse('chatbot:chatform'))
            else:
                # If error passwords, render the logerror page
                return render(request, 'chatbot/logerror.html')
        else:
            # Render the logerror page
            return render(request, 'chatbot/logerror.html')
    else:
        # Otherwise still in the index page
        return render(request, 'chatbot/index.html')


# View function of about function
def about(request):
    context_dict = {'boldmessage': '2663048X'}
    return render(request, 'chatbot/about.html', context=context_dict)


# View function of register function
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


def transform_to_text(my_queries):

    total_text_list = []
    if len(my_queries) != 0:
        for each in my_queries:
            current_text_list = []
            current_text_list += ["Address: " + each.property_address]
            current_text_list += ["City: " + each.property_city]
            current_text_list += ["Price: " + str(each.property_price)]
            current_text_list += ["Postcode: " + each.property_postcode]
            current_text_list += ["Property Type: " + each.property_type]
            current_text_list += ["Number of Bedroom: " + str(each.property_num_bedroom)]
            current_text_list += ["Post Time: " + str(each.property_date.date())]
            total_text_list += [current_text_list]
    else:
        total_text_list += [["Sorry, no such property which you prefer."]]
    return total_text_list


# Deal with the intent and do operate on database
def deal_with_intent(intent_name, para):
    global current_property
    global current_query
    text_list = None
    # The sell flow of intent detect
    if intent_name == "Sell":
        current_property = [None, None, None, None, None, None]
    if intent_name == "Sell_City":
        current_property[0] = para
    if intent_name == "Sell_Address":
        current_property[1] = para
    if intent_name == "Sell_Postcode":
        current_property[2] = para
    if intent_name == "Sell_Type":
        current_property[3] = para
    if intent_name == "Sell_BedroomNum":
        current_property[4] = para
    if intent_name == "Sell_Price":
        current_property[5] = para
    if intent_name == "Sell_Confirm_True":
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

    if intent_name == "Buy":
        current_query = [None, None, None, None, None, None]
    if intent_name == "Buy_City":
        current_query[0] = para
    if intent_name == "Buy_Postcode":
        current_query[1] = para
    if intent_name == "Buy_Type":
        current_query[2] = para
    if intent_name == "Buy_BedroomNum":
        current_query[3] = para
    if intent_name == "Buy_Min_Price":
        current_query[4] = para
    if intent_name == "Buy_Max_Price":
        current_query[5] = para

    if intent_name == "No_Max" or intent_name == "Buy_Max_Price":
        text_list = []
        if current_query[0] is not None:
            text_list += ["City: " + current_query[0]]
        if current_query[1] is not None:
            text_list += ["Postcode: " + current_query[1]]
        if current_query[2] is not None:
            text_list += ["Property type: " + current_query[2]]
        if current_query[3] is not None:
            text_list += ["Number of bedroom: " + str(current_query[3])]
        if current_query[4] is not None:
            text_list += ["Min Price: " + str(current_query[4])]
        if current_query[5] is not None:
            text_list += ["Max Price: " + str(current_query[5])]
        if len(text_list) > 0:
            return [text_list]

    if intent_name == "Buy_Query_True":
        p = Property.objects.filter()
        if current_query[0] is not None:
            p = p.filter(property_city=current_query[0])
        if current_query[1] is not None:
            p = p.filter(property_postcode__contains=current_query[1])
        if current_query[2] is not None:
            p = p.filter(property_type=current_query[2])
        if current_query[3] is not None:
            p = p.filter(property_num_bedroom=current_query[3])
        if current_query[4] is not None:
            p = p.filter(property_price__gte=current_query[4])
        if current_query[5] is not None:
            p = p.filter(property_price__lte=current_query[5])

        text_list = transform_to_text(p)
        return text_list

    if intent_name == "PreferFalse":

        p = Property.objects.order_by('?')[:4]
        text_list = transform_to_text(p)
        print(text_list)
        return text_list
    return text_list




@login_required
def chat(request):
    # Init intent name and parameter
    output_text = " "
    intent_name = None
    my_parameter = None

    # Init the chat input form
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

    my_response_words = deal_with_intent(intent_name, my_parameter)
    print(my_response_words)
    print(current_property)
    print(current_user)
    context_dict = {'output_text': output_text, 'my_response_words': my_response_words, 'form': form}
    return render(request, 'chatbot/chatform.html', context=context_dict)
