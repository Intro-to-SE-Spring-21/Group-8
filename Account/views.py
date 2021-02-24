from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Account.models import Follow

def register(request):

    if request.method == 'POST':
        #Attempt to create account
        form = UserCreationForm(request.POST)
        if form.is_valid():

            form.save()

            return HttpResponseRedirect('/')

    else:

        form = UserCreationForm()

    context = {'form':form}
    return render(request,'registration/register.html',context)  


def profile(request, username):

    
    user = get_object_or_404(User,username=username)
    following = len(Follow.objects.filter(following = user))
    return render(request,'Account/profile.html',{'user':user, 'following_count':following})