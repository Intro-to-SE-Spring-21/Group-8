from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Tweet

class Generate_Tweet(forms.Form):
    tweet_text = forms.CharField(max_length=280, label=False, widget=forms.Textarea(attrs={'placeholder': "What's happening?", 'style': 'resize: vertical', 'rows': 2,}))

    def info_return(self):
        data = self.cleaned_data['tweet_text']
        return data

class Account_Settings(forms.Form):
    Name = forms.CharField(initial='')