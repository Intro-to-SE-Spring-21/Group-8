
# templatetags/isFollowing.py

from django import template
from MainApp.models import Follow

register = template.Library()

@register.filter()
def isFollowing(user,otherAccount):
    if len(Follow.objects.filter(user=user,following=otherAccount)) == 1:
        return 1
    else:
        return 0