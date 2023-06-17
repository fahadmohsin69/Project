from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ContactMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout

from .models import Profile
from .forms import *


#Email Authentication 
import uuid
from django.conf import settings
from django.core.mail import send_mail


############################ Create your views here ##################################

def IndexPage(request):
    return render(request,'main/index.html')

def home_page(request):
    return render(request,'main_pages/home.html')

# Success Template view
def success(request):
    return render(request, "login_templates/success.html")

# token_send Template view
def token_send(request):
    return render(request, "login_templates/token_send.html")

# Update Password
def update(request):
    return render(request, "login_templates/update.html")

# Error Page
def error(request):
    return render(request, "login_templates/error.html")

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

############### User Side ##################

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
            user_obj.save()
            # profile_obj = UserMaster.objects.create(user = user_obj, auth_token = auth_token)
            # profile_obj.save()

            verification_email(email, auth_token, username)
            messages.success(request, 'Verification Email Sent! Check your Mail.')
            return redirect('token_send')

        except:
            return render('error')

    return render(request, "user/user_log_reg.html")


########### Login and SignUp Views ###########

# Login view
def login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)

            profile_obj = Profile.objects.filter(user = user).first()

            if user is not None:
                if profile_obj.is_verified:
                    Profile.objects.update(reset_password=False)
                    auth_login(request,user)
                    return redirect('/')
                else:
                    messages.error(request, 'You are not Verified! Please check Email.')
            else:
                messages.error(request, 'Invalid Username or Password!')
    except:
        messages.error(request, 'An Error Occured!')
        return redirect('/login')

    return render(request, "login_templates/login.html")

# SignUp view
def signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.ERROR, 'Username is already taken')
                return redirect('signup')

            if not username:
                messages.add_message(request, messages.ERROR, 'Username is required!')
                return redirect('signup')

            if not email:
                messages.add_message(request, messages.ERROR, 'Email is required!')
                return redirect('signup')
            
            if User.objects.filter(email=email).first():
                messages.add_message(request, messages.ERROR, 'Email is taken, try another one!')
                return redirect('signup')

            if len(password1) < 8:
                messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                return redirect('signup')
        
            if password1 != password2:
                messages.add_message(request, messages.ERROR, 'Password does not match')
                return redirect('signup')
            
            user_obj = User.objects.create_user(username=username, email=email, password=password1)
            user_obj.set_password(password1)

            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()

            verification_email(email, auth_token, username)
            messages.success(request, 'Check your E-mail for verification Code!')
            return redirect('/token_send')
            
        
        except Exception as e:
            print(e)

    return render(request, "login_templates/signup.html")

# Verification for Email
def verification_email(email,token, username):
    subject = 'Your account needs to be verified!'
    message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

#Verify Email Token
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your Account is already Verified!')
                return redirect('/login')
            
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Hurray! Your Account has been Verified!')
            return redirect('/success')
        
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/login')
    

# Forgot Password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).first():

            if Profile.objects.filter(is_verified=True):

                data = User.objects.get(email = email)
                auth_token = str(uuid.uuid4())
                
                Profile.objects.update(auth_token = auth_token)
            
                request.session['email'] = email
                username = data.username

                messages.success(request, 'We have sent you an Email with the Link!')

                password_verify(email, auth_token, username)
                return redirect('update')    
            else:
                messages.error(request, 'User is not verified yet!')
                return redirect('forgot_password')
        
        else:
            messages.error(request, "Invalid Email! Please enter valid E-mail")
            return redirect('forgot_password')
        
    return render(request, 'login_templates/forgot_password.html')

# Password Verify
def password_verify(email,token, username):
    subject = 'Request for Password Change!'
    message = f'Hi {username}! , Please use this link to reset your password: http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Reset Password 
def change_password(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.reset_password = True
            profile_obj.save()
            messages.success(request, 'Email Verified! Now you can change your Password.')
            return redirect('reset_password')
        else:
            return redirect('error')
    except Exception as e:
        print(e)

    return redirect('error')

# Reset Password
def reset_password(request):
    email = request.session['email']

    if request.method == 'POST':
        try:
            if Profile.objects.filter(reset_password=True):

                password = request.POST.get('password1')
                password1 = request.POST.get('password2')
                
                if len(password) < 8:
                    messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                    return redirect('reset_password')

                if password != password1:
                    messages.add_message(request, messages.ERROR, 'Password does not match')
                    return redirect('reset_password')

                user = User.objects.filter(email=email).first()
                user.set_password(password1)
                user.save()

                messages.success(request, 'Password Changed Successfully!')
                return redirect('login')
            
            else:
                messages.error(request, 'Email not verified yet!')
        except:
                messages.error(request, 'Update Error')
                return redirect('error')
        
    return render(request, 'login_templates/reset_password.html')