from django.urls import path
from chatbot import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('chatform/', views.chat, name='chatform'),
    path('logout/', views.user_logout, name='logout'),
]