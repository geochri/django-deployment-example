from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm



# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render (request,"basic_app/index.html")

@login_required
def special(request):
    return HttpResponse('You are logged in , Nice!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()

            #hash the password and save it!
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)

            #one to one relationship
            profile.user = user

            #profile picture
            if 'profile_pic' in request.FILES:
                print('found it!')

                #link the profile_pic with the request.FILES
                profile.profile_pic = request.FILES['profile_pic']

            #now we want to save the profile
            profile.save()
            #registration Successful
            registered = True

        #if one of them is invalid
        else:
            print(user_form.errors,profile_form.errors)



    else:
    #if method isnt POST we just render forms as blank! easy!
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'basic_app/register.html',
                           {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})




def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Account not active')
        else:
            print("Someone tried to login and failed")
            print("Username:{} and Password: {}".format(username,password))
            return HttpResponse('invalid login details supplied!')
    else:
        return render(request, 'basic_app/login.html',{})
