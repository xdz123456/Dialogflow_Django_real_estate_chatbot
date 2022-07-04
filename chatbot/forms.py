from django import forms
from chatbot.models import InputText


class InputTextForm(forms.ModelForm):
    input_text = forms.CharField(max_length=256, help_text="Chat with me")

    class Meta:
        model = InputText
        fields = ('input_text', )

    def __str__(self):
        return self.input_text




