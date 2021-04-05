import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Tweet
from .forms import Generate_Tweet, UserUpdateForm, TweetForm, RegisterForm
import random
from MainApp.models import Follow, Like, Retweet
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django.contrib.auth import get_user_model
User = get_user_model()
import collections

from itertools import chain

def register(request):

    if request.method == 'POST':
        #Attempt to create account
        form = RegisterForm(request.POST)
        if form.is_valid():

            form.save()

            return HttpResponseRedirect('/')

    else:

        form = RegisterForm()

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
        tweet = TweetForm(request.POST,request.FILES,user=request.user)
        
        if tweet.is_valid():
            print("savingggg")
            #new_tweet = Tweet.objects.create(tweet_creator=request.user, tweet_text=tweet.cleaned_data['tweet_text'], pub_date=datetime.datetime.now())
            tweet.save()


    def registerForm(self,request,button_name):
        """
        This function creates a user with the capability to insert the extra information.
        Inputs:
        - request: Django request output
        Returns:
        - Home render
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            form = UserCreationForm()

    def loginForm(self,request,button_name):
        """
        This function logs a user into the website.
        Inputs:
        - request: Django request output
        Returns:
        - Home render
        """
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            form = AuthenticationForm()

    def deleteTweet(self,request,button_name):
        """
        #TODO
        This function deletes a tweet object from the database
        Inputs:
        - 
        Returns:
        - 
        """
        #If the user is not authenticated, then just return since anonymous user is not allowed to remove like  
        if not request.user.is_authenticated:
            print("Error somewhere")
            return
 

        #When like button is submitted the value is in the form of: <username>,<postID>
        #Parse this value to get the appropiate user and post object.
        tweet_num = request.POST.get(button_name)
        
        tweet = Tweet.objects.get(pk=tweet_num)
        if tweet.tweet_creator != User:
            print("none authenticated deletion")

        tweet.delete()

    def getFollowRecommendations(self,request):
        """
        This function currently grabs three follower recommendations from the database.
        Each follower recommendation is unique and someone that the User does not currently follow
        Inputs:
        - request: Django request output
        Returns:
        - rand_three: dictionary containing three user objects as keys and whether or not the authenticated user folllows them as values
        """
        AllUsers = User.objects.all()
        #If user currently authenticated...remove from QuerySet since we do not want their own profile displayed in 'WhoToFollow'
        if request.user.is_authenticated:
            AllUsers = AllUsers.exclude(username=request.user.username)

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
            query = Follow(user=request.user,following=userToFollow,pub_date=datetime.datetime.now())
            query.save()
            #save the query

        return HttpResponseRedirect(reverse('MainApp:profile', args=[request.POST['follow']]))       

    def removeFollower(self,request,default_reverse='MainApp:profile',arg=None):
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
        if arg == None:
            arg = [request.POST['unfollow']]

        return HttpResponseRedirect(reverse(default_reverse, args=arg))

    def editAccount(self,request):
        """
        This function grabs the form data from the Settings tab, validates it, and saves the updates to the database
        Inputs:
        - request: Django request output
        Returns:
        - HttpResponseRedirect with the updated profile to be rendered
        """      

        edit = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if edit.is_valid():
            print("Valid")
            edit.save()    

      ## Here are some websites for editing the user information ##
    #### https://docs.djangoproject.com/en/3.1/topics/auth/default/#using-the-views #### 
    #### https://docs.djangoproject.com/en/3.1/topics/auth/default/ ####

        #reload the page and make sure an follow button shows back up
        return HttpResponseRedirect(reverse('MainApp:profile', args=[edit.cleaned_data['username']]))

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

        #{tweet_obj: {'type':'retweet',username:lmurdock12}}

        for tweet in Tweet.objects.order_by('-pub_date'):
            #If a user is logged in, and they have liked this specific tweet then set the tweet's value to 1
            if request.user.is_authenticated and Like.objects.filter(tweet=tweet,user=request.user):
                tweet_dict[tweet] = 1
            else:
                tweet_dict[tweet] = 0
        
        #Return the dictionary of tweets, and whether or not it has been liked by the authenticated user
        return tweet_dict

    def getPersonalFeed(self,request):
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

        #{tweet_obj: {'type':'retweet',username:lmurdock12}}
        following = Follow.objects.filter(user=request.user)
        print(following)

        #get random most recent 25 items or use ordered dict

        feed_data = []

        for follow in following:

            likes = Like.objects.filter(user=follow.following)
            retweets = Retweet.objects.filter(user=follow.following)
            tweets = Tweet.objects.filter(tweet_creator=follow.following)

            feed_data = feed_data + list(chain(likes,retweets,tweets))


        result_list = sorted(
            feed_data,
            key=lambda instance: instance.pub_date)

        print("######################")
        print(result_list)
        print("------------------")
        result_dict = {}

        for item in result_list:
            tmp_dict = {}

            if item.__class__.__name__ == "Tweet":

                tmp_dict['type'] = 'Tweet'
                tmp_dict['username'] = item.tweet_creator.username
                result_dict[item] = tmp_dict

            elif item.__class__.__name__ == "Like":

                tmp_dict['type'] = 'Like'
                tmp_dict['username'] = item.user.username
                result_dict[item.tweet] = tmp_dict

            elif item.__class__.__name__ == "Retweet":

                tmp_dict['type'] = 'Retweet'
                tmp_dict['username'] = item.user.username
                result_dict[item.tweet] = tmp_dict

        return result_dict

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
            new_like = Like(user=user,tweet=tweet,pub_date=datetime.datetime.now())
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

    def addRetweet(self,request,button_name):
        """
        This function creates and saves a Retweet object into the database.
        Inputs:
        - request: Django request output
        - button_name: The name of the button that is used in the POST request
        Returns:
        - None
        """    
        #If the user is not authenticated, then just return since anonymous user is not allowed to add retweet  
        if not request.user.is_authenticated:
            return

        #Passing in the name of the addRetweet button incase this button is named different things
        #across different pages.

        #When like button is submitted the value is in the form of: <username>,<postID>
        #Parse this value to get the appropiate user and post object.
        values = request.POST.get(button_name)

        #Username is index 0, postID is index 1
        val_dict = values.split(',') 
        
        user = User.objects.get(username=val_dict[0])
        tweet = Tweet.objects.get(pk=val_dict[1])

        #Check to make sure a Like object does not already exist for this post and user in the database
        if Retweet.objects.filter(user=user,tweet=tweet):
            print("This user has already liked that tweet")
        else:
            new_retweet = Retweet(user=user,tweet=tweet,pub_date=datetime.datetime.now())
            new_retweet.save()        

    def removeRetweet(self,request,button_name):
        """
        This function removes a retweet object from the database.
        Inputs:
        - request: Django request output
        - button_name: The name of the button that is used in the POST request
        Returns:
        - None
        """    
        #If the user is not authenticated, then just return since anonymous user is not allowed to remove retweet  
        if not request.user.is_authenticated:
            return
             #Passing in the name of the addLike button incase this button is named different things
        #across different pages.

        #When retweet button is submitted the value is in the form of: <username>,<postID>
        #Parse this value to get the appropiate user and post object.
        values = request.POST.get(button_name)

        #Username is index 0, postID is index 1
        val_dict = values.split(',') 
        
        user = User.objects.get(username=val_dict[0])
        tweet = Tweet.objects.get(pk=val_dict[1])

        #finding retweet and deleting
        old_retweet = Retweet.objects.get(user=user,tweet=tweet)
        old_retweet.delete()        


class MainPage(GenericPage):

    def get(self,request):
        """
        This function handles a get request for the homepage
        Inputs:
        - request: Django request output
        Returns:
        - render() function call with the page to be rendered
        """
        
        if "feedType" in request.COOKIES:
            if request.COOKIES['feedType'] == 'personal' and request.user.is_authenticated:
                tweetFeed = self.getPersonalFeed(request)
            else:
                tweetFeed = self.getFeed(request)
        else:
            tweetFeed = self.getFeed(request)

        tweet_form = TweetForm(user=request.user)
        
        rand_three = self.getFollowRecommendations(request)  

        AllUsers = User.objects.all()

        register_form = RegisterForm()

        login_form = AuthenticationForm()

        ### Variable declared to pass all information to webpage
        #TODO: rename tweet to tweet_form
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three,
        'tweetFeed':tweetFeed, 'tweet':tweet_form, 'AllUsers':AllUsers, 'register':register_form,
        'login':login_form}

        if request.user.is_authenticated:

            profile_user = get_object_or_404(User,username=request.user.username)
            #How many users is the profile user following
            self.getFollowCounts(profile_user,context)
            context['validSession'] = True


        ### Render the webpage
        page_render = render(request,'MainApp/homepage.html', context)
        if "feedType" not in request.COOKIES:
            page_render.set_cookie("feedType","global")

        return page_render

    @method_decorator(login_required)
    def post(self,request):
        """
        This function handles a post request for the homepage
        Inputs:
        - request: Django request output
        Returns:
        - self.get() which renders the rest of the page
        """


        #Creating a Tweet through the webpage
        
        if request.POST.get("like_button"):
            self.addLike(request,"like_button")

        if request.POST.get("unlike_button"):
            self.removeLike(request,"unlike_button")
        
        if request.method == "POST":
            self.createTweet(request)

        if request.POST.get('delete_button'):
            self.deleteTweet(request,'delete_button')

        if request.POST.get('login_button'):
            self.loginForm(request, 'login_button')

        if request.POST.get('register_button'):
            self.registerForm(request, 'register_button')

        if request.POST.get("retweet_button"):
            self.addRetweet(request,"retweet_button")
        
        if request.POST.get("unretweet_button"):
            self.removeRetweet(request,"unretweet_button")

        if request.POST.get("switch-feed"):

            response = HttpResponseRedirect("/")
            if request.COOKIES['feedType'] == "global":
                response.set_cookie("feedType","personal")
            else:
                response.set_cookie("feedType","global")
            
            return response

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

        tweet_form = TweetForm(user=request.user)

        profile_user = get_object_or_404(User,username=username)
        #How many users is the profile user following
        following = Follow.objects.filter(user = profile_user)
        #how many people are following the profile user
        followed_by = Follow.objects.filter(following=profile_user)

        #Get likes
        liked_tweets = Like.objects.filter(user=profile_user)


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

        AllUsers = User.objects.all()

        register_form = RegisterForm()

        login_form = AuthenticationForm()
        
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
            'profile_user':profile_user,'auth_follow':auth_follow, 'tweet':tweet_form,
            'isNative':isNative, 'personalscroll':UserTweets, 'clickedtab':1, 
            'liked_tweets_len':len(liked_tweets), 'AllUsers':AllUsers, 'register':register_form,
            'login':login_form}
           
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

        if request.POST.get("like_button"):
            self.addLike(request,"like_button")

        if request.POST.get("unlike_button"):
            self.removeLike(request,"unlike_button")

        if request.POST.get("retweet_button"):
            self.addRetweet(request,"retweet_button")
        
        if request.POST.get("unretweet_button"):
            self.removeRetweet(request,"unretweet_button")

        #Creating a Tweet through the webpage
        if request.POST.get('submit_tweet'):
            self.createTweet(request)

        if request.POST.get('delete_button'):
            self.deleteTweet(request,'delete_button')

        if request.POST.get('login_button'):
            self.loginForm(request, 'login_button')

        if request.POST.get('register_button'):
            self.registerForm(request, 'register_button')

        return self.get(request, request.user.username)


class ProfileFollowing(GenericPage):

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
        liked_tweets = Like.objects.filter(user=profile_user)


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

        rand_three = self.getFollowRecommendations(request)
        
        AllUsers = User.objects.all()

        register_form = RegisterForm()

        login_form = AuthenticationForm()
        
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
            'profile_user':profile_user,'auth_follow':auth_follow, 'clickedtab':3,
            'isNative':isNative, 'following':following, 'followers':followed_by, 
            'AllUsers':AllUsers,"liked_tweets_len":len(liked_tweets),
            'register':register_form, 'login':login_form}

           
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
            return self.removeFollower(request,'MainApp:followingtab',arg=[request.user])

        if request.POST.get("like_button"):
            self.addLike(request,"like_button")

        if request.POST.get("unlike_button"):
            self.removeLike(request,"unlike_button")

        if request.POST.get('login_button'):
            self.loginForm(request, 'login_button')

        if request.POST.get('register_button'):
            self.registerForm(request, 'register_button')
     
        return self.get(request, request.user.username)


class ProfileFollowers(GenericPage):

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
        followed_by = Follow.objects.filter(following = profile_user)
        liked_tweets = Like.objects.filter(user=profile_user)
 
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

        rand_three = self.getFollowRecommendations(request)

        AllUsers = User.objects.all()

        register_form = RegisterForm()

        login_form = AuthenticationForm()
        
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
            'profile_user':profile_user,'auth_follow':auth_follow, 'clickedtab':2,
            'isNative':isNative, 'followers': followed_by, 'following':following,
            'AllUsers':AllUsers,"liked_tweets_len":len(liked_tweets),
            'register':register_form, 'login':login_form}

           
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
            return self.removeFollower(request,'MainApp:followerstab',arg=[request.user])

        if request.POST.get("like_button"):
            self.addLike(request,"like_button")

        if request.POST.get("unlike_button"):
            self.removeLike(request,"unlike_button")

        if request.POST.get('login_button'):
            self.loginForm(request, 'login_button')

        if request.POST.get('register_button'):
            self.registerForm(request, 'register_button')
     
        return self.get(request, request.user.username)


class ProfileSettings(GenericPage):

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
        liked_tweets = Like.objects.filter(user=profile_user)

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

        rand_three = self.getFollowRecommendations(request)

        #Grab the initial values to pass to the user form
        initial_dict = {
            "first_name" : request.user.first_name,
            "last_name"  : request.user.last_name,
            "email" : request.user.email,
            "username"  : request.user.username,
            "bio": request.user.bio,
            "profileImage": request.user.profileImage,
        }

        edit_form = UserUpdateForm(initial = initial_dict,instance=request.user)
        
        AllUsers = User.objects.all()

        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
            'profile_user':profile_user,'auth_follow':auth_follow, 'clickedtab':4,
            'isNative':isNative, 'form':edit_form, 'AllUsers':AllUsers}

           
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


        if request.POST.get('submit_user_edits'):
            return self.editAccount(request)

        return self.get(request, request.user.username)
      
      
class ProfileLikes(GenericPage):

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
        

    def getProfileLikes(self,request,profile_user):
        

        #With user I can grab all of the Likes a given user have
        #With each Like I can loop and grab the specific tweet
        liked_tweet_obj_dict = {}
        #".liked_user" grabs all the like objects for the given profile_user
        for like in profile_user.liked_user.all():
            tweet_obj = like.tweet
            #If a user is logged in, and they have liked this specific tweet then set the tweet's value to 1
            if request.user.is_authenticated and Like.objects.filter(tweet=tweet_obj,user=request.user):
                liked_tweet_obj_dict[tweet_obj] = 1
            else:
                liked_tweet_obj_dict[tweet_obj] = 0

        #Return the dictionary of tweets, and whether or not it has been liked by the authenticated user
        return liked_tweet_obj_dict


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


        liked_tweet_obj_dict = self.getProfileLikes(request,profile_user)

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

        rand_three = self.getFollowRecommendations(request)

        register_form = RegisterForm()

        login_form = AuthenticationForm()
        
        context = {'validSession':False, 'username':request.user.username, 'whoToFollow':rand_three, 
            'profile_user':profile_user,'auth_follow':auth_follow,
            'isNative':isNative, 'clickedtab':5,'liked_tweet_obj_dict':liked_tweet_obj_dict, 
            'liked_tweets_len':len(liked_tweets), 'register':register_form, 'login':login_form}
           
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

        if request.POST.get("unlike_button"):
            self.removeLike(request,"unlike_button")

        if request.POST.get('delete_button'):
            self.deleteTweet(request,'delete_button')

        if request.POST.get('login_button'):
            self.loginForm(request, 'login_button')

        if request.POST.get('register_button'):
            self.registerForm(request, 'register_button')
            
        if request.POST.get("retweet_button"):
            self.addRetweet(request,"retweet_button")
        
        if request.POST.get("unretweet_button"):
            self.removeRetweet(request,"unretweet_button")


        return self.get(request, request.user.username)

