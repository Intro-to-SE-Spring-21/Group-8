import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tweet(models.Model):
    tweet_creator = models.ForeignKey(User, on_delete=models.PROTECT)
    tweet_text = models.CharField(max_length=280)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return "{} - Post id - {}".format(self.tweet_creator, self.pk)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
