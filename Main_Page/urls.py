from django.urls import path
from . import views

app_name = 'Main_Page'
urlpatterns = [
    path('',views.index,name='index'),
]