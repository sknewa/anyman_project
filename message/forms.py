from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    body = forms.CharField(label="Your Custom Label:", widget=forms.Textarea)  # Customize label here

    class Meta:
        model = Message
        fields = ['recipient', 'body']
        help_texts = {
            'body': 'Enter your message here.',
        }
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Type your message...'})
        }