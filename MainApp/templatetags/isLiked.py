

# templatetags/isLiked.py

from django import template

register = template.Library()

@register.filter()
def isLiked(tweet, user):
    if len(tweet.tweet.filter(user=user)) == 1:
        return 1
    else:
        return 0