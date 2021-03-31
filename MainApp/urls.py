from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from MainApp.views import MainPage, ProfilePage, ProfileFollowing, ProfileFollowers, ProfileSettings, ProfileLikes
app_name = 'MainApp'
urlpatterns = [
    path('',MainPage.as_view(),name='homepage'), 
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view() ,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('<str:username>/',ProfilePage.as_view(),name='profile'),
    path('<str:username>/settings',ProfileSettings.as_view(),name='settingstab'),
    path('<str:username>/following',ProfileFollowing.as_view(),name='followingtab'),
    path('<str:username>/likes',ProfileLikes.as_view(),name='likestab'),
    path('<str:username>/followers',ProfileFollowers.as_view(),name='followerstab')

]
