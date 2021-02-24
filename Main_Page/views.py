from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random


def index(request):

    AllUsers = User.objects.all()
    rand_three = []
    for i in range(3):
        temp = random.choice(AllUsers)
        while temp in rand_three or temp.username == request.user.username:
            temp = random.choice(AllUsers)
        rand_three.append(temp)
        

    context = {'validSession':False, 'username':request.user.username, 'userdic':AllUsers, 'userlist':rand_three}

    if(request.user.is_authenticated):
        context['validSession'] = True

    return render(request,'Main_Page/index.html',context)
    #return HttpResponse("Hello world.")