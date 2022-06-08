from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import Student, Student_Record_Form
from django.contrib.auth import authenticate, login

def index (response):
    return render (response, 'api/index.html',)

def signin (request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        auth = get_user_model()
        
        user = auth.authenticate(username=username, password=password)

        print(username)

        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("/")
    else:
        return render(request, '/')

def signup (request):
    if request.method == "POST":
        return render(request, 'api/home.html', )
    else:
        return render(request, 'api/signup.html',)

def home(response):
    return render(response, 'api/home.html', )