import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tweet
from .forms import Generate_Tweet
import random
from MainApp.models import Follow, Like
from django.urls import reverse

##New includes
from django.views.generic import TemplateView
import collections


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

class GenericPage(TemplateView):


    def createTweet(self,request):
        """
        This function creates and saves a Tweet object into the database.
        Inputs:
        - request: Django request output
        Returns:
        - None
        """
        tweet = Generate_Tweet(request.POST)
        if tweet.is_valid():
            new_tweet = Tweet.objects.create(tweet_creator=request.user, tweet_text=tweet.cleaned_data['tweet_text'], pub_date=datetime.datetime.now())
            new_tweet.save()


    def deleteTweet(self,request):
        """
        #TODO
        This function deletes a tweet object from the database
        Inputs:
        - 
        Returns:
        - 
        """
        pass


    def getFollowRecommendations(self,request):
        """
        This function currently grabs three follower recommendations from the database.
        Normally this function would return three NEW people to follow, but currently
        this function just returns three new or currently followed people while we wait
        for additional website functionality to be implemented
        #TODO: Reset to regular functionality once follower tabs built
        Inputs:
        - request: Django request output
        Returns:
        - rand_three: dictionary containing three user objects as keys and whether or not the authenticated user folllows them as values
        """
        AllUsers = User.objects.all()
        #If user currently authenticated...remove from QuerySet since we do not want their own profile displayed in 'WhoToFollow'
        if request.user.is_authenticated:
            AllUsers.exclude(username=request.user.username)
        
        rand_three = []
        #####
        # We are temporarily showing accounts a user already follows or does not follow...until additional website functionaility is added
        #####
        #Keep looping until we either gather 3 new users to follow or run out of options with who to follow (Since the user follows everyone)
        if request.user.is_authenticated:
            AllUsers = AllUsers.exclude(username=request.user.username)
        AllUsers = AllUsers.exclude(username=request.user.username)
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

        return rand_three


    def getFollowCounts(self,profile_user,context):

        #How many users is the profile user following
        following = Follow.objects.filter(user = profile_user)
        context['following_len'] = len(following)
        #how many people are following the profile user
        followed_by = Follow.objects.filter(following=profile_user)
        context['followed_by_len'] = len(followed_by)


    def addFollower(self,request):
        """
        This function adds a Follower for the given authenticated user
        Inputs:
        - request: Django request output
        Returns:
        - HttpResponseRedirect with the profile to be rendered
        """
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

        return HttpResponseRedirect(reverse('MainApp:profile', args=[request.POST['follow']]))       


    def removeFollower(self,request):
        """
        This function removes a Follower for the given authenticated user
        Inputs:
        - request: Django request output
        Returns:
        - HttpResponseRedirect with the profile to be rendered
        """       
        userToUnfollow = User.objects.get(username=request.POST['unfollow'])
        #Relationship should already exist.
        unfollow = Follow.objects.filter(user=request.user,following=userToUnfollow)
        unfollow.delete()

        #reload the page and make sure an follow button shows back up
        return HttpResponseRedirect(reverse('MainApp:profile', args=[request.POST['unfollow']]))

    def getFeed(self,request):
        """
        This function returns a feed of tweets to display to a page.
        Currently just gets all the tweets and sorts them by publication date.
        Will add more complex capabilities in future.
        Inputs:
        - None
        Returns:
        - Dicitonary of Tweet keys and values of whether or not the authenticated user has liked the tweet.
        """
        #Create a dictionary with each key being a tweet, and each value being whether or not the authetnicated user has liked that tweet.
        #This is so we can appropriately display either the like or the unlike button with a tweet.

        tweet_dict = {}

        for tweet in Tweet.objects.order_by('-pub_date'):
            #If a user is logged in, and they have liked this specific tweet then set the tweet's value to 1
            if request.user.is_authenticated and Like.objects.filter(tweet=tweet,user=request.user):
                tweet_dict[tweet] = 1
            else:
                tweet_dict[tweet] = 0
        
        #Return the dictionary of tweets, and whether or not it has been liked by the authenticated user
        return tweet_dict


    def addLike(self,request,button_name):
        """
        This function creates and saves a Like object into the database.
        Inputs:
        - request: Django request output
        - button_name: The name of the button that is used in the POST request
        Returns:
        - None
        """    
        #If the user is not authenticated, then just return since anonymous user is not allowed to add like  
        if not request.user.is_authenticated:
            return

        #Passing in the name of the addLike button incase this button is named different things
        #across different pages.

        #When like button is submitted the value is in the form of: <username>,<postID>
        #Parse this value to get the appropiate user and post object.
        values = request.POST.get(button_name)

        #Username is index 0, postID is index 1
        val_dict = values.split(',') 
        
        user = User.objects.get(username=val_dict[0])
        tweet = Tweet.objects.get(pk=val_dict[1])

        #Check to make sure a Like object does not already exist for this post and user in the database
        if Like.objects.filter(user=user,tweet=tweet):
            print("This user has already liked that tweet")
        else:
            new_like = Like(user=user,tweet=tweet)
            new_like.save()
        

    
    def removeLike(self,request,button_name):
        """
        This function removes a like object from the database.
        Inputs:
        - request: Django request output
        - button_name: The name of the button that is used in the POST request
        Returns:
        - None
        """    
        #If the user is not authenticated, then just return since anonymous user is not allowed to remove like  
        if not request.user.is_authenticated:
            return
             #Passing in the name of the addLike button incase this button is named different things
        #across different pages.

        #When like button is submitted the value is in the form of: <username>,<postID>
        #Parse this value to get the appropiate user and post object.
        values = request.POST.get(button_name)

        #Username is index 0, postID is index 1
        val_dict = values.split(',') 
        
        user = User.objects.get(username=val_dict[0])
        tweet = Tweet.objects.get(pk=val_dict[1])

        #finding liked tweet and deleting
        old_like = Like.objects.get(user=user,tweet=tweet)
        old_like.delete()


class MainPage(GenericPage):

    def get(self,request):
        """
        This function handles a get request for the homepage
        Inputs:
        - request: Django request output
        Returns:
        - render() function call with the page to be rendered
        """

        tweet_form = Generate_Tweet()
        
        tweetFeed = self.getFeed(request)
        rand_three = self.getFollowRecommendations(request)  
        ### Variable declared to pass all information to webpage
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three,
        'tweetFeed':tweetFeed, 'tweet':tweet_form}

        if request.user.is_authenticated:
            profile_user = get_object_or_404(User,username=request.user.username)
            #How many users is the profile user following
            self.getFollowCounts(profile_user,context)
            context['validSession'] = True


        ### Render the webpage
        return render(request,'MainApp/homepage.html', context)
    

    def post(self,request):
        """
        This function handles a post request for the homepage
        Inputs:
        - request: Django request output
        Returns:
        - self.get() which renders the rest of the page
        """
        #Creating a Tweet through the webpage
        if request.POST.get("submit_tweet"):
            self.createTweet(request)

        if request.POST.get("like_button"):
            self.addLike(request,"like_button")

        if request.POST.get("unlike_button"):
            self.removeLike(request,"unlike_button")

        return self.get(request)


class ProfilePage(GenericPage):

    def getUserTweets(self,request,profile_user):
        """ 
        This function grabs all the tweets from a specific user
        Inputs:
        - profile_user: The desired User object
        Returns:
        - QuerySet with all the User's tweets
        """

        tweet_dict = {}

        for tweet in Tweet.objects.order_by('-pub_date').filter(tweet_creator=profile_user.pk):
            #If a user is logged in, and they have liked this specific tweet then set the tweet's value to 1
            if request.user.is_authenticated and Like.objects.filter(tweet=tweet,user=request.user):
                tweet_dict[tweet] = 1
            else:
                tweet_dict[tweet] = 0
        
        #Return the dictionary of tweets, and whether or not it has been liked by the authenticated user
        return tweet_dict
        

    def get(self,request,username):
        """
        This function handles a get request for the profile page
        Inputs:
        - request: Django request output
        Returns:
        - render() function call with the page to be rendered
        """
        context = {}
        profile_user = get_object_or_404(User,username=username)
        #How many users is the profile user following
        following = Follow.objects.filter(user = profile_user)
        #how many people are following the profile user
        followed_by = Follow.objects.filter(following=profile_user)

        #Get likes
        liked_tweets = Like.objects.filter(user=profile_user)
        print(liked_tweets)

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

        UserTweets = self.getUserTweets(request,profile_user)

        rand_three = self.getFollowRecommendations(request)
        
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
            'profile_user':profile_user,'auth_follow':auth_follow,
            'isNative':isNative, 'personalscroll':UserTweets,'liked_tweets_len':len(liked_tweets)}
           
        self.getFollowCounts(profile_user,context)


        if(request.user.is_authenticated):
            context['validSession'] = True
        
        return render(request,'MainApp/profile.html', context)


    def post(self,request,username):
        """
        This function handles a post request for the homepage
        Inputs:
        - request: Django request output
        - username: the 'username' found in profile/<username/ in the url
        Returns:
        - self.get() which renders the rest of the page
        """
        
        if not request.user.is_authenticated:
            #If the user tries to POST anything and they are not logged in, redirect them to the login page
            #at some point look at the thing that will redirect them back to the same page and complete the previous
            #action once they are logged in
            return HttpResponseRedirect(reverse('MainApp:login'))

        if request.POST.get('follow'):

            return self.addFollower(request)

        if request.POST.get('unfollow'):
            
            return self.removeFollower(request)

        return self.get(request)