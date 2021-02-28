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

    profile_user = get_object_or_404(User,username=request.user.username)

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

    # List of all users (Helpful for many functions)
    AllUsers = User.objects.all()

    ## Random 3 Users selected for 'Who to Follow'
    rand_three = []
    for i in range(3):
        temp = random.choice(AllUsers)
        while temp in rand_three or temp.username == request.user.username:
            temp = random.choice(AllUsers)
        rand_three.append(temp)

    #How many users is the profile user following
    following = Follow.objects.filter(user = profile_user)
    #how many people are following the profile user
    followed_by = Follow.objects.filter(following=profile_user)

    ### Variable declared to pass all information to webpage
    context = {'validSession':False, 'username':request.user.username, 'userdic':AllUsers, 
    'userlist':rand_three, 'explorescroll':AllTweets, 'tweet':tweet, 
    'following_len':len(following),'followed_by_len':len(followed_by)}

    
    ## Check if a user is logged in
    if(request.user.is_authenticated):
        context['validSession'] = True

    ### Render the webpage
    return render(request,'Main_Page/index.html', context) 


