from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Account'
urlpatterns = [
    #path('',views.index,name='index'), #TODO: Make this into a 404 or something /accounts by itself should not do anything
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view() ,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('<str:username>/',views.native_profile,name='profile'),
    path('<str:username>/',views.foreign_profile,name='view profile')

]
