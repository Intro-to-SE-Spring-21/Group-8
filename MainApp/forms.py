from django import forms
from django.forms import fields
from django.utils import timezone
from .models import Tweet
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import datetime

#Get the updated user model
from django.contrib.auth import get_user_model
User = get_user_model()


from django.forms.widgets import FileInput


class Generate_Tweet(forms.Form):
    tweet_text = forms.CharField(max_length=280, label=False, widget=forms.Textarea(attrs={'placeholder': "What's happening?", 'style': 'resize: vertical', 'rows': 2,}))

    def info_return(self):
        data = self.cleaned_data['tweet_text']
        return data

class TweetForm(forms.ModelForm):
    """Proper form for creating a tweet"""
    class Meta:
        model = Tweet
        fields = ('tweet_text','tweet_image')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TweetForm, self).__init__(*args, **kwargs)
        self.fields['tweet_text'] = forms.CharField(max_length=280, label=False, widget=forms.Textarea(attrs={'placeholder': "What's happening?", 'style': 'resize: vertical', 'rows': 2,}))
        

    def save(self, *args, **kwargs):
        print(self.fields['tweet_image'])
        self.instance.tweet_creator = self.user
        self.instance.pub_date=datetime.datetime.now()
        tweet = super(TweetForm, self).save(*args, **kwargs)
        return tweet


class UserUpdateForm(forms.ModelForm):
    """The Model form for updating user profile settings,
        Additional attributes to edit can be added in 'fields' dict (must be in User Object)"""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','bio', 'profileImage']

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
