import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Account.models import Tweet
from .forms import Generate_Tweet
import random
from Account.models import Follow
from django.urls import reverse



def index(request):

    ## Creating a Tweet through the webpage
    if request.method == "POST":
        tweet = Generate_Tweet(request.POST)
        if tweet.is_valid():
            new_tweet = Tweet.objects.create(tweet_creator=request.user, tweet_text=tweet.cleaned_data['tweet_text'], pub_date=datetime.datetime.now())
            tweet = Generate_Tweet()
            pass
    else:
        tweet = Generate_Tweet()


    ## Explore Page Scroll
    AllTweets = Tweet.objects.order_by('-pub_date') 

    AllUsers = User.objects.all()
    #If user currently authenticated...remove from QuerySet since we do not want their own profile displayed in 'WhoToFollow'
    if request.user.is_authenticated:
        AllUsers.exclude(username=request.user.username)
    rand_three = []
    #Keep looping until we either gather 3 new users to follow or run out of options with who to follow (Since the user follows everyone)
    while len(rand_three) < 3 and len(AllUsers) > 0:

        #Grab random user
        temp = random.choice(AllUsers)
        #If we have an authenticated user currently logged in...check to see if we already follow this temp user
        if request.user.is_authenticated and Follow.objects.filter(user=request.user, following=temp):
            #Remove temp usery from Queryset if we already do
            AllUsers = AllUsers.exclude(username=temp.username)
            continue
        #If temp is a correct user that we can follow..remove it from QuerySet and add it to the rand_three list
        AllUsers = AllUsers.exclude(username=temp.username)
        rand_three.append(temp)

    ### Variable declared to pass all information to webpage
    context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three,
     'explorescroll':AllTweets, 'tweet':tweet}

    if request.user.is_authenticated:
        profile_user = get_object_or_404(User,username=request.user.username)
        #How many users is the profile user following
        following = Follow.objects.filter(user = profile_user)
        context['following_len'] = len(following)
        #how many people are following the profile user
        followed_by = Follow.objects.filter(following=profile_user)
        context['followed_by_len'] = len(followed_by)

    
    ## Check if a user is logged in
    if(request.user.is_authenticated):
        context['validSession'] = True

    ### Render the webpage
    return render(request,'Main_Page/index.html', context) 


