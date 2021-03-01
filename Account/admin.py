from django.contrib import admin

from .models import Follow
from .models import Tweet

admin.site.register(Tweet)
admin.site.register(Follow)