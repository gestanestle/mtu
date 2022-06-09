from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import Student, Student_Record_Form
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required

def index (response):
    return render (response, 'api/index.html',)

def signin (request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        
        user = authenticate(user_name=user_name, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('/')
    else:
        return redirect('/')

def signup (request):
    if request.method == "POST":
        student_no = request.POST['student_no']
        user_name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password']


        student_instance = list(Student.objects.filter(student_no=student_no))
        if (len(student_instance) != 0):
            new_user = User.objects.create_user(student_no=Student.objects.get(student_no=student_no) , user_name=user_name, email=email, password=password)
            new_user.save()
            messages.success(request, "Account successfully created.")
        else:
            messages.error(request, "Invalid Student Number")
        return redirect('/')
    else:
        return render(request, 'api/signup.html',)

@login_required
def home(response):
    return render(response, 'api/home.html', )

@login_required
def signout(request):
    logout(request)
    return redirect('/')