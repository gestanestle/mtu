from audioop import reverse
from email import message
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import Student, Student_Record_Form
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse


def index (response):
    return render (response, 'api/index.html',)

def signin (request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        
        user = authenticate(user_name=user_name, password=password)
        
        if user is not None:
            if user.is_email_verified:    
                login(request, user)
                return redirect("/home")
        
        messages.error(request, "Invalid credentials.")
        return redirect('/')
    else:
        return redirect('/')

def send_verification_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('api/activate.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk,)),
        'token':generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


def activate_user(request, uidb64, token):
  
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  

    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.success(request, "Email has been verified, you can now login.")
        return redirect(reverse('signin'))

    else:
        print(generate_token.check_token(user, token))
        return render(request, 'api/activation-failed.html', {'user':user})

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
            send_verification_email(new_user, request)
            messages.success(request, "We sent you an email. Please verify your account.")
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

