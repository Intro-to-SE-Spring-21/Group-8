from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Account.models import Follow
from django.urls import reverse

def register(request):

    if request.method == 'POST':
        #Attempt to create account
        form = UserCreationForm(request.POST)
        if form.is_valid():

            form.save()

            return HttpResponseRedirect('/')

    else:

        form = UserCreationForm()

    context = {'form':form}
    return render(request,'registration/register.html',context)  


def profile(request, username):

    if request.method == "POST":
        
        if not request.user.is_authenticated:
            #If the user tries to POST anything and they are not logged in, redirect them to the login page
            #at some point look at the thing that will redirect them back to the same page and complete the previous
            #action once they are logged in
            return HttpResponseRedirect(reverse('Account:login'))

        if request.POST['followProfileSubmit']:
            print(request.POST)

            #Create query
            #user = current session user
            #following: is the user profile
            userToFollow = User.objects.get(username=request.POST['followProfileSubmit'])
            
            
            #make sure relationship does not already exist
            old_follow = Follow.objects.filter(user=request.user,following=userToFollow)
            #Check to make sure they are not equal
            if(userToFollow.username != request.user.username and not old_follow):
                print("Successfully meet criteria to follow")
                query = Follow(user=request.user,following=userToFollow)
                query.save()
                #save the query
                
        #reload the page and make sure an unfollow button shows up 
        return HttpResponseRedirect(reverse('Account:profile', args=[request.POST['followProfileSubmit']]))
            

    user = get_object_or_404(User,username=username)
    following = len(Follow.objects.filter(following = user))
    return render(request,'Account/profile.html',{'user':user, 'following_count':following})