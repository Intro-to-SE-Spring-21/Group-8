from django import forms
from django.utils import timezone
from .models import Tweet
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

#Get the updated user model
from django.contrib.auth import get_user_model
User = get_user_model()

class Generate_Tweet(forms.Form):
    tweet_text = forms.CharField(max_length=280, label=False, widget=forms.Textarea(attrs={'placeholder': "What's happening?", 'style': 'resize: vertical', 'rows': 2,}))

    def info_return(self):
        data = self.cleaned_data['tweet_text']
        return data

class UserUpdateForm(forms.ModelForm):
    """The Model form for updating user profile settings,
        Additional attributes to edit can be added in 'fields' dict (must be in User Object)"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','bio']

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
