from django.urls import path
from chatbot import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),
]