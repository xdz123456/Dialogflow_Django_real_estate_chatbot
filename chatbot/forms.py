from django import forms
from django.contrib.auth.models import User

from chatbot.models import InputText


class InputTextForm(forms.ModelForm):
    input_text = forms.CharField(max_length=256, help_text="Chat with me now",
                                 widget=forms.TextInput(attrs={'placeholder': 'Chat with the Real Estate Chatbot'}))

    class Meta:
        model = InputText
        fields = ('input_text',)

    def __str__(self):
        return self.input_text


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        help_texts = {
            'username': None,
        }
