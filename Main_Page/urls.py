from django.urls import path, re_path
from . import views

app_name = 'Main_Page'
urlpatterns = [
    path('',views.index,name='index'),
]

