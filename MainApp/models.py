import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django import template

class User(AbstractUser):
    """This model extands the base User object...adding a User bio
        ***This model acts the exact same as the original User, except it now has the additional bio attribute***

        TODO: Add profile pic place to this model
    """
    bio = models.TextField(max_length=150,blank=True)


class Tweet(models.Model):
    tweet_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.TextField(max_length=280)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return "Post # {} by {}".format(self.pk, self.tweet_creator)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def visible_info(self):
        if not self.tweet_text:
            return
        return self.tweet_text

    def countLikes(self):
        return len(Like.objects.filter(tweet=self))

    def countRetweets(self):
        return len(Retweet.objects.filter(tweet=self))

    likes = property(countLikes)   
    retweets = property(countRetweets) 

class Follow(models.Model):
    user = models.ForeignKey(User, related_name = "user", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name = "following", on_delete=models.CASCADE)
    

    def __str__(self):
        return "User {} - Following - {} - {} ".format(self.user.username,self.following.username,self.pk)


class Like(models.Model):
    user = models.ForeignKey(User,related_name="liked_user",on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet,related_name="tweet",on_delete=models.CASCADE)

    def __str__(self):
        return "User {} liked Tweet #: {}".format(self.user.username,self.tweet.pk)


class Retweet(models.Model):
    user = models.ForeignKey(User,related_name="retweetingUser",on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet,related_name="retweetedTweet",on_delete=models.CASCADE)

    def __str__(self):
        return "User {} retweeted Tweet #: {}".format(self.user.username,self.tweet.pk)
