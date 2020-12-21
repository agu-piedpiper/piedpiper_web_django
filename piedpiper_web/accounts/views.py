from django.shortcuts import render
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login

# Create your views here.

def login_form(request):
    return render(request, 'accounts/login_form.html',)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return render(request, 'cms/activity_list.html',)
        ...
    else:
        # Return an 'invalid login' error message.
         return render(request, 'accounts/login_form.html',)

def logout(request):

   return render(request, 'accounts/login_form.html',)
    