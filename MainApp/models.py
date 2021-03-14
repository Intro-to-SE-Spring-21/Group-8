import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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