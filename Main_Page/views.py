from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm

def index(request):

    context = {'validSession':False}

    if(request.user.is_authenticated):
        context['validSession'] = True

    return render(request,'Main_Page/index.html',context)
    #return HttpResponse("Hello world.")