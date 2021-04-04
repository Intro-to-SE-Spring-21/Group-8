

# templatetags/isRetweeted.py

from django import template

register = template.Library()

@register.filter()
def isRetweeted(tweet, user):
    if len(tweet.retweetedTweet.filter(user=user)) == 1:
        return 1
    else:
        return 0