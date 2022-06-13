from audioop import reverse
from email import message
from email.policy import default
from multiprocessing.dummy import current_process
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import Upload_Image, User, Student_Record_Form
from django.contrib.auth import authenticate, login, logout
from .models import User, Student, Student_Record
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.forms.models import model_to_dict


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

def home(request):
    user = request.user
    image_form = Upload_Image()

    if request.method == "POST":
        current_pass = request.POST['current_pass']
        pass_1 = request.POST['pass_1']
        pass_2 = request.POST['pass_2']

        to_auth = authenticate(user_name=user.user_name, password=current_pass)

        if to_auth is None:
            messages.error(request, "Incorrect current passowrd.")
            return redirect('/home')

        if pass_1 != pass_2:
            messages.error(request, "Passwords don't match")
            return redirect('/home')

        modify_user = User.objects.get(student_no= user.student_no_id)
        modify_user.set_password(pass_1)
        modify_user.save() 
        user.password = modify_user.password
        messages.success(request, "Passowrd has been reset.")
    
    context = {
        'nbar':'home',
        'user':user,
        'image_form':image_form,
    }

    return render(request, 'api/account.html', context)


def profile(request):
    user = request.user
    
    if request.method == "POST":
        return
        
    record = Student_Record.objects.get(student_no=user.student_no_id)
    srf = Student_Record_Form(initial=model_to_dict(record))

    context = {
        'nbar':'profile',
        'user':user,
        'srf':srf,
    }

    return render(request, 'api/profile.html', context)

def display_own_grades(response):
    context = {
        'nbar':'display_own_grades',
    }
    return render(response, 'api/display_own_grades.html', context)

def individual_evaluation_report(response):
    context = {
        'nbar':'individual_evaluation_report',
    }
    return render(response, 'api/individual_evaluation_report.html', context)

def faculty_evaluation(response):
    context = {
        'nbar':'faculty_evaluation',
    }
    return render(response, 'api/faculty_evaluation.html', context)

def ledger_of_accounts(response):
    context = {
        'nbar':'ledger_of_accounts'
    }
    return render(response, 'api/ledger_of_accounts.html', context)

def transactions(response):
    context = {
        'nbar':'transactions'
    }
    return render(response, 'api/transactions.html', context)

def apply_for_graduation(response):
    context = {
        'nbar':'apply_for_graduation'
    }
    return render(response, 'api/apply_for_graduation.html', context)


def signout(request):
    logout(request)
    return redirect('/')


def upload_pfp(request):
    if request.method == "POST":
        user = request.user
        # profile_image = request.POST.get('profile_image', 'default.jpg')
        # profile_image = request.POST.get('profile')
        modify_user = User.objects.get(student_no=user.student_no_id)
        # updated_request = request.POST.copy()
        # updated_request.update({'student_no': user.student_no_id})
        form = Upload_Image(request.POST, request.FILES ,instance=modify_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Changed pfp")
        else:
            print(form.errors.as_data())
            messages.error(request, "Invalid file format.")

    return redirect('/home')
