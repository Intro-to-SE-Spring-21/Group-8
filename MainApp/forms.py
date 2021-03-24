from django import forms
from django.utils import timezone
from .models import Tweet
from django.contrib.auth.forms import UserChangeForm

#Get the updated user model
from django.contrib.auth import get_user_model
User = get_user_model()

class Generate_Tweet(forms.Form):
    tweet_text = forms.CharField(max_length=280, label=False, widget=forms.Textarea(attrs={'placeholder': "What's happening?", 'style': 'resize: vertical', 'rows': 2,}))

    def info_return(self):
        data = self.cleaned_data['tweet_text']
        return data

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','bio']


