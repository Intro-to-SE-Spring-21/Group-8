from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random
from Account.models import Follow
from Account.models import Tweet
from django.urls import reverse



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

    profile_user = get_object_or_404(User,username=username)
    #How many users is the profile user following
    following = Follow.objects.filter(user = profile_user)
    #how many people are following the profile user
    followed_by = Follow.objects.filter(following=profile_user)
    
    
    if request.method == "POST":
        
        if not request.user.is_authenticated:
            #If the user tries to POST anything and they are not logged in, redirect them to the login page
            #at some point look at the thing that will redirect them back to the same page and complete the previous
            #action once they are logged in
            return HttpResponseRedirect(reverse('Account:login'))

        if request.POST.get('follow'):

            #Create query
            #user = current session user
            #following: is the user profile
            userToFollow = User.objects.get(username=request.POST['follow'])
            
            
            #make sure relationship does not already exist
            old_follow = Follow.objects.filter(user=request.user,following=userToFollow)
            #Check to make sure they are not equal
            if(userToFollow.username != request.user.username and not old_follow):
                print("Successfully meet criteria to follow")
                query = Follow(user=request.user,following=userToFollow)
                query.save()
                #save the query

            return HttpResponseRedirect(reverse('Account:profile', args=[request.POST['follow']]))

        if request.POST.get('unfollow'):
            
            userToUnfollow = User.objects.get(username=request.POST['unfollow'])

            #Relationship should already exist.
            unfollow = Follow.objects.filter(user=request.user,following=userToUnfollow)
            unfollow.delete()
       
            #reload the page and make sure an follow button shows back up

            return HttpResponseRedirect(reverse('Account:profile', args=[request.POST['unfollow']]))

    
    #if current_user is in followed_by...show unfollow
    #Check to see if we are on the users native profile if they are logged in
    isNative = False
    #Stores whether or not the authenticated user is following the current profile user
    auth_follow = False
    if request.user.is_authenticated:
        if request.user.username == profile_user.username:
            isNative = True
            
        #Check to see if the authenticated user is already following the user
        for followed in followed_by:
            if request.user == followed.user:
                auth_follow = True

    UserTweets = Tweet.objects.order_by('-pub_date').filter(tweet_creator=profile_user.pk)

    AllUsers = User.objects.all()
    #If user currently authenticated...remove from QuerySet since we do not want their own profile displayed in 'WhoToFollow'
    if request.user.is_authenticated:
        AllUsers.exclude(username=request.user.username)
    
    rand_three = []
    #####
    # We are temporarily showing accounts a user already follows or does not follow...until additional website functionaility is added
    #####
    #Keep looping until we either gather 3 new users to follow or run out of options with who to follow (Since the user follows everyone)
    while len(rand_three) < 3 and len(AllUsers) > 0:
        #Grab random user
        temp = random.choice(AllUsers)
        tmp_dict = {temp:False}
        #If we have an authenticated user currently logged in...check to see if we already follow this temp user
        if request.user.is_authenticated and Follow.objects.filter(user=request.user, following=temp):
            #Temporarily allow users we already follow.
            tmp_dict[temp] = True
            rand_three.append(tmp_dict)
            #Remove temp usery from Queryset if we already do
            AllUsers = AllUsers.exclude(username=temp.username)
            continue
        #If temp is a correct user that we can follow..remove it from QuerySet and add it to the rand_three list
        AllUsers = AllUsers.exclude(username=temp.username)
        rand_three.append(tmp_dict)


    context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
    'profile_user':profile_user,'auth_follow':auth_follow, 'following_len':len(following),'followed_by_len':len(followed_by),
    'isNative':isNative, 'personalscroll':UserTweets}
    
    if(request.user.is_authenticated):
        context['validSession'] = True
    
    return render(request,'Account/profile.html', context)


#@register.filter(name='return_item')
#def return_item(l, i):
#    try:
#        return l[i]
#    except:
#        return None

