from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This will become the Live Scroll of Tweets")
