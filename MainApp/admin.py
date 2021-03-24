from django.contrib import admin


from .models import Follow, Tweet, Like, User


#Imports required so we can edit our custom User model that includes bio
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

#Get the current User model in use
User = get_user_model()

#Override UserChangeForm and Admin interface for the User model and add the bio attribute
#See: https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('bio',)}),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Tweet)
admin.site.register(Follow)
admin.site.register(Like)
