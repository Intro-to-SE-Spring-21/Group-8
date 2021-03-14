from django.contrib import admin

from .models import Follow, Tweet, Like


admin.site.register(Tweet)
admin.site.register(Follow)
admin.site.register(Like)