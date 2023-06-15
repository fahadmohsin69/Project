from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages
from django.contrib.auth.models import User

from .models import *
from .forms import *


#Email Authentication 
import uuid
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def IndexPage(request):
    return render(request,'main/index.html')

def home_page(request):
    return render(request,'main_pages/home.html')

def contact_us(request):
    if request.method == 'POST':
        if request.method == 'POST':
            first_name = request.POST.get('first_name', '')
            print(first_name)
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            contact_message = ContactMessage(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
            contact_message.save()
            return render(request, 'main/main.html',{'success': True})
    else:
        return render(request, 'main/main.html',{'success': False})

############### Engineer Side ###############

def Engin_Log_Reg_Tem(request):
    return render(request, "engineer/engineer_log_reg.html")

############### User Side ###############

def User_Log_Reg_Tem(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'Username is already taken')
                return redirect('register')

            if not username:
                messages.add_message(request, messages.ERROR, 'Username is required!')
                return redirect('register')

            if not email:
                messages.add_message(request, messages.ERROR, 'Email is required!')
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'Email already exists, user another one.')
                return redirect('register')

            if len(password1) < 8:
                messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                return redirect('register')
        
            if password1 != password2:
                messages.add_message(request, messages.ERROR, 'Password does not match')
                return redirect('register')
            
            user_obj = User.objects.create_user(username=username, email=email, password=password1)
            auth_token = str(uuid.uuid4())

            profile_obj = UserMaster.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()

            verification_email(email, auth_token, username)
            messages.success(request, 'Verification Email Sent! Check your Mail.')
            return redirect('register')

        except:
            return render('error')

    return render(request, "user/user_log_reg.html")

# Verification for Email
def verification_email(email,token, username):
    subject = 'Your account needs to be verified'
    message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Verify Email Token
def verify(request, auth_token):
    try:
        profile_obj = UserMaster.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your Account has been Verified!')
            return redirect('login_signup')
        else:
            return redirect('error')
    except Exception as e:
        print(e)