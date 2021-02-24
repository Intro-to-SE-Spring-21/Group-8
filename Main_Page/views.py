from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Account.models import Tweet
import random


def index(request):

    if request.method == "POST":
        print('Hello')#Create Tweet Button

    AllTweets = Tweet.objects.order_by('-pub_date')

    AllUsers = User.objects.all()
    rand_three = []
    for i in range(3):
        temp = random.choice(AllUsers)
        while temp in rand_three or temp.username == request.user.username:
            temp = random.choice(AllUsers)
        rand_three.append(temp)
        

    context = {'validSession':False, 'username':request.user.username, 'userdic':AllUsers, 
    'userlist':rand_three, 'explorescroll':AllTweets}

    if(request.user.is_authenticated):
        context['validSession'] = True

    return render(request,'Main_Page/index.html', context)
    #return HttpResponse("Hello world.")


