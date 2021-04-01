from django.test import TestCase, Client
from django.urls import reverse
from MainApp.models import Like,Tweet,User,Follow


class TestHomepageView(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse('MainApp:homepage')


        #Create three test users
        self.user_1 = User.objects.create(username='lmurdock12',first_name='Lucian',last_name='Murdock',email='lcm388@msstate.edu')
        self.user_1.set_password('lmurdock12')
        self.user_1.save()
        self.user_2 = User.objects.create(username='bhball22',first_name='Brandon',last_name='Ball',email='bhbal22@msstate.edu')
        self.user_2.set_password('bhball22')
        self.user_2.save()
        self.user_3 = User.objects.create(username='natalie2by4',first_name='Natalie',last_name='Albritton',email='natalie2by4@msstate.edu')
        self.user_3.set_password('natalie2by4')
        self.user_3.save()

        #Create some test posts
        self.post_1 = Tweet.objects.create(tweet_creator=User.objects.get(pk=1), tweet_text="Recent extreme weather events are a stark reminder that we’re already seeing the effects of climate change here at home and around the world. This type of observation system will help scientists monitor and predict future weather events.", pub_date='2021-02-26 10:30:00.000000')
        self.post_2 = Tweet.objects.create(tweet_creator=User.objects.get(pk=1), tweet_text="To avoid a climate disaster, we need to eliminate emissions from the ways we create electricity, grow food, make things, move around, and heat and cool our buildings. It won’t be easy, but I believe we can do it. This book is about what it will take.", pub_date='2021-02-14 09:17:00.000000')
        self.post_3 = Tweet.objects.create(tweet_creator=User.objects.get(pk=2), tweet_text="I want a chance to do for you what you do for me! #QueenSugar", pub_date='2021-02-16 08:00:00.000000')
        self.post_4 = Tweet.objects.create(tweet_creator=User.objects.get(pk=2), tweet_text="The path to a stronger, healthier life, begins with the love we bring ourselves. Which is why this Valentine’s Day weekend, @ww_us and I are hosting Oprah’s Your Life In Focus: Be The Love You Need, a live virtual experience that will help you activate the life you most desire.", pub_date='2021-02-4 08:16:00.000000')
        self.post_5 = Tweet.objects.create(tweet_creator=User.objects.get(pk=3), tweet_text="Some of our favorite moments from the #GitHubUniverse keynote. See the full version and all sessions, now on demand, githubuniverse.com", pub_date='2020-12-14 11:02:00.000000')
        self.post_6 = Tweet.objects.create(tweet_creator=User.objects.get(pk=3), tweet_text="Congrats on 20 years!", pub_date="2021-02-22 16:15:00.000000")
        
        #Create some test likes
        self.like_1 = Like.objects.create(tweet=self.post_1,user=self.user_1)


    def test_homepage_GET(self):

        #Test homepage as if the user was not currently logged in
        response = self.client.get(self.homepage_url)

        #ValidSession should be false since no user is logged in right now
        self.assertEqual(response.context['validSession'],False)
        
        #Who to follow should return 3 users to display 
        self.assertEqual(len(response.context['whoToFollow']),3)


        #Check to make sure the page loaded successfully
        self.assertEquals(response.status_code,200)
        #Check to make sure the right template was loaded
        self.assertTemplateUsed(response,'MainApp/homepage.html')

        #Assert that the 6 tweets in the database get returned to the template
        self.assertEqual(len(response.context['tweetFeed']),6)

    def test_homepage_tweet_POST(self):

        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')

        curr_num_tweets = len(Tweet.objects.all())

        # 'tweet_text': ['dfd'], 'submit_tweet': ['1']}>
        response = self.client.post(self.homepage_url, {
            'submit_tweet':['1'],
            'tweet_text':['test']
        })

        #Check to make sure number of tweets increased by 1
        self.assertEqual(len(Tweet.objects.all()),curr_num_tweets+1)

        #Make sure the specific tweet we created was added to database
        tweet_obj = Tweet.objects.filter(tweet_text='test').exists()
        self.assertTrue(tweet_obj)


        #Create a tweet but not logged in...assert that this fails

    def test_homepage_like_POST(self):

        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_likes = len(Like.objects.all())
        
        response = self.client.post(self.homepage_url, {
            'like_button':['lmurdock12,3']
        })

        new_num_likes = len(Like.objects.all())

        #Check to make sure one more like was added to database
        self.assertEqual(curr_num_likes+1,new_num_likes)

        #Get the like object that should have been created
        liked_tweet = Tweet.objects.get(pk=3)
        user_that_liked = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the like object was correctly created
        new_like = Like.objects.filter(tweet=liked_tweet,user=user_that_liked).exists()
    
        #Check to make sure the like exists
        self.assertTrue(new_like)

    def test_homepage_unlike_POST(self):
        

        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_likes = len(Like.objects.all())
        
        #Simulate unliking the test like that was created
        response = self.client.post(self.homepage_url, {
            'unlike_button':['lmurdock12,1']
        })

        new_num_likes = len(Like.objects.all())

        #Check to make sure one Like was removed to database
        self.assertEqual(curr_num_likes-1,new_num_likes)

        #Get the like object that should have been created
        liked_tweet = Tweet.objects.get(pk=1)
        user_that_liked = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the like object was correctly created
        new_like = Like.objects.filter(tweet=liked_tweet,user=user_that_liked).exists()
    
        #Check to make sure the like no longer exists
        self.assertFalse(new_like)


class TestProfileView(TestCase):

    def setUp(self):
        self.client = Client()

        self.profile_url = reverse('MainApp:profile',args=['lmurdock12'])
        self.likeTab_url = reverse('MainApp:likestab',args=['lmurdock12'])
        self.followingTab_url = reverse('MainApp:followingtab',args=['lmurdock12'])
        self.followerTab_url = reverse('MainApp:followerstab',args=['lmurdock12'])

        #Create three test users
        self.user_1 = User.objects.create(username='lmurdock12',first_name='Lucian',last_name='Murdock',email='lcm388@msstate.edu')
        self.user_1.set_password('lmurdock12')
        self.user_1.save()
        self.user_2 = User.objects.create(username='bhball22',first_name='Brandon',last_name='Ball',email='bhbal22@msstate.edu')
        self.user_2.set_password('bhball22')
        self.user_2.save()
        self.user_3 = User.objects.create(username='natalie2by4',first_name='Natalie',last_name='Albritton',email='natalie2by4@msstate.edu')
        self.user_3.set_password('natalie2by4')
        self.user_3.save()

        #Create some test posts
        self.post_1 = Tweet.objects.create(tweet_creator=User.objects.get(pk=1), tweet_text="Recent extreme weather events are a stark reminder that we’re already seeing the effects of climate change here at home and around the world. This type of observation system will help scientists monitor and predict future weather events.", pub_date='2021-02-26 10:30:00.000000')
        self.post_2 = Tweet.objects.create(tweet_creator=User.objects.get(pk=1), tweet_text="To avoid a climate disaster, we need to eliminate emissions from the ways we create electricity, grow food, make things, move around, and heat and cool our buildings. It won’t be easy, but I believe we can do it. This book is about what it will take.", pub_date='2021-02-14 09:17:00.000000')
        self.post_3 = Tweet.objects.create(tweet_creator=User.objects.get(pk=2), tweet_text="I want a chance to do for you what you do for me! #QueenSugar", pub_date='2021-02-16 08:00:00.000000')
        self.post_4 = Tweet.objects.create(tweet_creator=User.objects.get(pk=2), tweet_text="The path to a stronger, healthier life, begins with the love we bring ourselves. Which is why this Valentine’s Day weekend, @ww_us and I are hosting Oprah’s Your Life In Focus: Be The Love You Need, a live virtual experience that will help you activate the life you most desire.", pub_date='2021-02-4 08:16:00.000000')
        self.post_5 = Tweet.objects.create(tweet_creator=User.objects.get(pk=3), tweet_text="Some of our favorite moments from the #GitHubUniverse keynote. See the full version and all sessions, now on demand, githubuniverse.com", pub_date='2020-12-14 11:02:00.000000')
        self.post_6 = Tweet.objects.create(tweet_creator=User.objects.get(pk=3), tweet_text="Congrats on 20 years!", pub_date="2021-02-22 16:15:00.000000")
        
        #Create some test likes
        self.like_1 = Like.objects.create(tweet=self.post_1,user=self.user_1)

        #Create some follows
        #self.follow_1 = Follow.objects.create(user=self.user_1,following=self.user_3)


    def test_fakeProfile_GET(self):

        #Try to get a profile that does not actually exist
        self.fake_url = reverse('MainApp:profile',args=['sgsdf'])
        response = self.client.get(self.fake_url)

        #Should return a 404 error since no user 'sgsdf' actually exists
        self.assertEquals(response.status_code,404)


    def test_profile_GET(self):

        #Test homepage as if the user was not currently logged in
        response = self.client.get(self.profile_url)

        #ValidSession should be false since no user is logged in right now
        self.assertEqual(response.context['validSession'],False)
        
        #Who to follow should return 3 users to display 
        self.assertEqual(len(response.context['whoToFollow']),3)

        #Make sure that the two tweets made by the user are displayed on personal scroll
        self.assertEqual(len(response.context['personalscroll']),2)

        #Check to make sure the page loaded successfully
        self.assertEquals(response.status_code,200)
        #Check to make sure the right template was loaded
        self.assertTemplateUsed(response,'MainApp/profile.html')


    def test_profile_tweet_POST(self):

        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')

        curr_num_tweets = len(Tweet.objects.all())

        # 'tweet_text': ['dfd'], 'submit_tweet': ['1']}>
        response = self.client.post(self.profile_url, {
            'submit_tweet':['1'],
            'tweet_text':['test']
        })

        #Check to make sure number of tweets increased by 1
        self.assertEqual(len(Tweet.objects.all()),curr_num_tweets+1)

        #Make sure the specific tweet we created was added to database
        tweet_obj = Tweet.objects.filter(tweet_text='test').exists()
        self.assertTrue(tweet_obj)


    def test_profile_follow_POST(self):
        
        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_follows = len(Follow.objects.all())
        
        response = self.client.post(self.profile_url, {
            'follow':['bhball22']
        })

        new_num_follows = len(Follow.objects.all())

        #Check to make sure one more follow was added to database
        self.assertEqual(curr_num_follows+1,new_num_follows)

        #Get the follow object that should have been created
        user_followed = User.objects.get(username="bhball22")
        user = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the follow object was correctly created
        new_follow = Follow.objects.filter(user=user,following=user_followed).exists()
    
        #Check to make sure the follow exists
        self.assertTrue(new_follow)

        Follow.objects.filter(user=user,following=user_followed).delete()


    def test_profile_unfollow_POST(self):

        self.follow_1 = Follow.objects.create(user=self.user_1,following=self.user_3)

        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_follows = len(Follow.objects.all())
        
        #Simulate unfollowing the test Follow relationship that was created
        response = self.client.post(self.profile_url, {
            'unfollow':['natalie2by4']
        })

        new_num_follows = len(Follow.objects.all())

        #Check to make sure one Follow was removed from database
        self.assertEqual(curr_num_follows-1,new_num_follows)

        #Get the like object that should have been created
        user = User.objects.get(username="lmurdock12")
        user_followed = User.objects.get(username="natalie2by4")

        #get the True or false depending whether the like object was correctly created
        removed_follow = Follow.objects.filter(user=user,following=user_followed).exists()
    
        #Check to make sure the like no longer exists
        self.assertFalse(removed_follow)

    def test_profile_like_POST(self):

        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_likes = len(Like.objects.all())
        
        response = self.client.post(self.profile_url, {
            'like_button':['lmurdock12,3']
        })

        new_num_likes = len(Like.objects.all())

        #Check to make sure one more like was added to database
        self.assertEqual(curr_num_likes+1,new_num_likes)

        #Get the like object that should have been created
        liked_tweet = Tweet.objects.get(pk=3)
        user_that_liked = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the like object was correctly created
        new_like = Like.objects.filter(tweet=liked_tweet,user=user_that_liked).exists()
    
        #Check to make sure the like exists
        self.assertTrue(new_like)

    def test_profile_unlike_POST(self):

        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_likes = len(Like.objects.all())
        
        #Simulate unliking the test like that was created
        response = self.client.post(self.profile_url, {
            'unlike_button':['lmurdock12,1']
        })

        new_num_likes = len(Like.objects.all())

        #Check to make sure one Like was removed to database
        self.assertEqual(curr_num_likes-1,new_num_likes)

        #Get the like object that should have been created
        liked_tweet = Tweet.objects.get(pk=1)
        user_that_liked = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the like object was correctly created
        new_like = Like.objects.filter(tweet=liked_tweet,user=user_that_liked).exists()
    
        #Check to make sure the like no longer exists
        self.assertFalse(new_like)

    def test_followerTab_follow_POST(self):

        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_follows = len(Follow.objects.all())
        
        response = self.client.post(self.followerTab_url, {
            'follow':['bhball22']
        })

        new_num_follows = len(Follow.objects.all())

        #Check to make sure one more follow was added to database
        self.assertEqual(curr_num_follows+1,new_num_follows)

        #Get the follow object that should have been created
        user_followed = User.objects.get(username="bhball22")
        user = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the follow object was correctly created
        new_follow = Follow.objects.filter(user=user,following=user_followed).exists()
    
        #Check to make sure the follow exists
        self.assertTrue(new_follow)

        Follow.objects.filter(user=user,following=user_followed).delete()

    def test_followerTab_unfollow_POST(self):
        
        self.follow_1 = Follow.objects.create(user=self.user_1,following=self.user_3)

        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_follows = len(Follow.objects.all())
        
        #Simulate unfollowing the test Follow relationship that was created
        response = self.client.post(self.followerTab_url, {
            'unfollow':['natalie2by4']
        })

        new_num_follows = len(Follow.objects.all())

        #Check to make sure one Follow was removed from database
        self.assertEqual(curr_num_follows-1,new_num_follows)

        #Get the like object that should have been created
        user = User.objects.get(username="lmurdock12")
        user_followed = User.objects.get(username="natalie2by4")

        #get the True or false depending whether the like object was correctly created
        removed_follow = Follow.objects.filter(user=user,following=user_followed).exists()
    
        #Check to make sure the like no longer exists
        self.assertFalse(removed_follow)
    
    def test_followingTab_unfollow_POST(self):
        #Note: can not follow a user from followingTab unless from whotofollow 
        self.follow_1 = Follow.objects.create(user=self.user_1,following=self.user_3)

        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_follows = len(Follow.objects.all())
        
        #Simulate unfollowing the test Follow relationship that was created
        response = self.client.post(self.followingTab_url, {
            'unfollow':['natalie2by4']
        })

        new_num_follows = len(Follow.objects.all())

        #Check to make sure one Follow was removed from database
        self.assertEqual(curr_num_follows-1,new_num_follows)

        #Get the like object that should have been created
        user = User.objects.get(username="lmurdock12")
        user_followed = User.objects.get(username="natalie2by4")

        #get the True or false depending whether the like object was correctly created
        removed_follow = Follow.objects.filter(user=user,following=user_followed).exists()
    
        #Check to make sure the like no longer exists
        self.assertFalse(removed_follow)

    def test_followerTab_follow_POST(self):

        #Temporary login user
        response = self.client.login(username='lmurdock12',password='lmurdock12')
        
        curr_num_follows = len(Follow.objects.all())
        
        response = self.client.post(self.followingTab_url, {
            'follow':['bhball22']
        })

        new_num_follows = len(Follow.objects.all())

        #Check to make sure one more follow was added to database
        self.assertEqual(curr_num_follows+1,new_num_follows)

        #Get the follow object that should have been created
        user_followed = User.objects.get(username="bhball22")
        user = User.objects.get(username="lmurdock12")
        #get the True or false depending whether the follow object was correctly created
        new_follow = Follow.objects.filter(user=user,following=user_followed).exists()
    
        #Check to make sure the follow exists
        self.assertTrue(new_follow)

        Follow.objects.filter(user=user,following=user_followed).delete()


#test profileLike like 
#test profileLike unlike

#test profile settings eventually

#check number of follows,num of likes, etc.
#Followers tab gets all the people that follow a certain user
#Following tab gets all the people that currently authenticated user is following
