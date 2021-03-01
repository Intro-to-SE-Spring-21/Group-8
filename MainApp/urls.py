from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'MainApp'
urlpatterns = [
    path('',views.index,name='index'), 
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view() ,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('<str:username>/',views.profile,name='profile')

]