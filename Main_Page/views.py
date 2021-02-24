from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Account.models import Tweet
import random


def index(request):

    ## Creating a Tweet through the webpage
    if request.method == "POST":
        print('Hello')#Create Tweet Button

    ## Explore Page Scroll
    AllTweets = Tweet.objects.order_by('-pub_date') 

    # List of all users (Helpful for many functions)
    AllUsers = User.objects.all()

    ## Random 3 Users selected for 'Who to Follow'
    rand_three = []
    for i in range(3):
        temp = random.choice(AllUsers)
        while temp in rand_three or temp.username == request.user.username:
            temp = random.choice(AllUsers)
        rand_three.append(temp)
        

    ### Variable declared to pass all information to webpage
    context = {'validSession':False, 'username':request.user.username, 'userdic':AllUsers, 
    'userlist':rand_three, 'explorescroll':AllTweets}

    ## Check if a user is logged in
    if(request.user.is_authenticated):
        context['validSession'] = True

    ### Render the webpage
    return render(request,'Main_Page/index.html', context)


