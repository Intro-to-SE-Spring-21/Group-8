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

    #username = request.user.username
    #profile_user = get_object_or_404(User,username=username)

    ## Creating a Tweet through the webpage
    if request.method == "POST":
        tweet = Generate_Tweet(request.POST)
        if tweet.is_valid():
            new_tweet = Tweet.objects.create(tweet_creator=request.user, tweet_text=tweet.cleaned_data['tweet_text'], pub_date=datetime.datetime.now())
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

    #profile_user = request.user.username
    #profile_user = get_object_or_404(User,username=username)
    #How many users is the profile user following
    #following = Follow.objects.filter(user = profile_user)
    #how many people are following the profile user
    #followed_by = Follow.objects.filter(following=profile_user)

    ### Variable declared to pass all information to webpage
    context = {'validSession':False, 'username':request.user.username, 'userdic':AllUsers, 
    'userlist':rand_three, 'explorescroll':AllTweets, 'tweet':tweet}
    #'following_len':len(following),'followed_by_len':len(followed_by)}

    
    ## Check if a user is logged in
    if(request.user.is_authenticated):
        context['validSession'] = True

    ### Render the webpage
    return render(request,'Main_Page/index.html', context) 
    #{'profile_user':profile_user, 'following_len':len(following), 'followed_by_len':len(followed_by)})
    #, {'following_len':len(following),'followed_by_len':len(followed_by)})

def main(request, username):

     if request.method == "POST":
        
        if not request.user.is_authenticated:
            #If the user tries to POST anything and they are not logged in, redirect them to the login page
            #at some point look at the thing that will redirect them back to the same page and complete the previous
            #action once they are logged in
            return HttpResponseRedirect(reverse('Account:login'))

        if request.POST.get('followProfileSubmit'):

            #Create query
            #user = current session user
            #following: is the user profile
            userToFollow = User.objects.get(username=request.POST['followProfileSubmit'])
            
            
            #make sure relationship does not already exist
            old_follow = Follow.objects.filter(user=request.user,following=userToFollow)
            #Check to make sure they are not equal
            if(userToFollow.username != request.user.username and not old_follow):
                print("Successfully meet criteria to follow")
                query = Follow(user=request.user,following=userToFollow)
                query.save()
                #save the query

            return HttpResponseRedirect(reverse('Main_Page:index', args=[request.POST['followProfileSubmit']]))

        if request.POST.get('unfollowProfileSubmit'):
            
            userToUnfollow = User.objects.get(username=request.POST['unfollowProfileSubmit'])

            #Relationship should already exist.
            unfollow = Follow.objects.filter(user=request.user,following=userToUnfollow)
            unfollow.delete()
       
            #reload the page and make sure an follow button shows back up
            return HttpResponseRedirect(reverse('Main_Page:index', args=[request.POST['unfollowProfileSubmit']]))
    
        profile_user = get_object_or_404(User,username=username)
        #How many users is the profile user following
        following = Follow.objects.filter(user = profile_user)
        #how many people are following the profile user
        followed_by = Follow.objects.filter(following=profile_user)

        #if current_user is in followed_by...show unfollow

        #Check to see if we are on the users native profile if they are logged in
        isNative = False
        auth_follow = False
        if request.user.is_authenticated:
            if request.user.username == profile_user.username:
                isNative = True

                #Check to see if the authenticated user is already following the user
                for followed in followed_by:
                    if request.user == followed.user:
                        auth_follow = True
        return render(request,'Main_Page/index.html',{'profile_user':profile_user,'auth_follow':auth_follow, 'following_len':len(following),'followed_by_len':len(followed_by),'isNative':isNative})


