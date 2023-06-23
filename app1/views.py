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

########### Login and SignUp Views for User ###########

def user_login(request):
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
        return redirect('/user_login')

    return render(request, "user/user_login.html")

# SignUp view
def user_signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.ERROR, 'Username is already taken')
                return redirect('user_signup')

            if not username:
                messages.add_message(request, messages.ERROR, 'Username is required!')
                return redirect('user_signup')

            if not email:
                messages.add_message(request, messages.ERROR, 'Email is required!')
                return redirect('user_signup')
            
            if User.objects.filter(email=email).first():
                messages.add_message(request, messages.ERROR, 'Email is taken, try another one!')
                return redirect('user_signup')

            if len(password1) < 8:
                messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                return redirect('user_signup')
        
            if password1 != password2:
                messages.add_message(request, messages.ERROR, 'Password does not match')
                return redirect('user_signup')
            
            user_obj = User.objects.create_user(username=username, email=email, password=password1)
            user_obj.set_password(password1)

            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()

            user_verification_email(email, auth_token, username)
            messages.success(request, 'Check your E-mail for verification Code!')
            return redirect('/user_token_send')
            
        
        except Exception as e:
            print(e)

    return render(request, "user/user_signup.html")

# Verification for Email
def user_verification_email(email,token, username):
    subject = 'Your account needs to be verified!'
    message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/user_verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

#Verify Email Token
def user_verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your Account is already Verified!')
                return redirect('/user_login')
            
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Hurray! Your Account has been Verified!')
            return redirect('/user_success')
        
        else:
            return redirect('user_error')
    except Exception as e:
        print(e)
        return redirect('/user_login')
    
# Forgot Password
def user_forgot_password(request):
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

                engineer_password_verify(email, auth_token, username)
                return redirect('user_update')    
            else:
                messages.error(request, 'User is not verified yet!')
                return redirect('user_forgot_password')
        
        else:
            messages.error(request, "Invalid Email! Please enter valid E-mail")
            return redirect('user_forgot_password')
        
    return render(request, 'user/user_forgot_password.html')

# Password Verify
def user_password_verify(email,token, username):
    subject = 'Request for Password Change!'
    message = f'Hi {username}! , Please use this link to reset your password: http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Reset Password 
def user_change_password(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.reset_password = True
            profile_obj.save()
            messages.success(request, 'Email Verified! Now you can change your Password.')
            return redirect('user_reset_password')
        else:
            return redirect('user_error')
    except Exception as e:
        print(e)

    return redirect('user_error')

# Reset Password
def user_reset_password(request):
    email = request.session['email']

    if request.method == 'POST':
        try:
            if Profile.objects.filter(reset_password=True):

                password = request.POST.get('password1')
                password1 = request.POST.get('password2')
                
                if len(password) < 8:
                    messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                    return redirect('user_reset_password')

                if password != password1:
                    messages.add_message(request, messages.ERROR, 'Password does not match')
                    return redirect('user_reset_password')

                user = User.objects.filter(email=email).first()
                user.set_password(password1)
                user.save()

                messages.success(request, 'Password Changed Successfully!')
                return redirect('user_login')
            
            else:
                messages.error(request, 'Email not verified yet!')
        except:
                messages.error(request, 'Update Error')
                return redirect('user_error')
        
    return render(request, 'user/user_reset_password.html')

# Success Template view
def user_success(request):
    return render(request, "user/user_success.html")

# token_send Template view
def user_token_send(request):
    return render(request, "user/user_token_send.html")

# Update Password
def user_update(request):
    return render(request, "user/user_update.html")

# Error Page
def user_error(request):
    return render(request, "user/user_error.html")


def User_Log_Reg_Tem(request):
    return render(request, "user/user_log_reg.html")


########### Login and SignUp Views for Engineer ###########

# Login view
def engineer_login(request):
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
        return redirect('/engineer_login')

    return render(request, "engineer/engineer_login.html")

# SignUp view
def engineer_signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.ERROR, 'Username is already taken')
                return redirect('engineer_signup')

            if not username:
                messages.add_message(request, messages.ERROR, 'Username is required!')
                return redirect('engineer_signup')

            if not email:
                messages.add_message(request, messages.ERROR, 'Email is required!')
                return redirect('engineer_signup')
            
            if User.objects.filter(email=email).first():
                messages.add_message(request, messages.ERROR, 'Email is taken, try another one!')
                return redirect('engineer_signup')

            if len(password1) < 8:
                messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                return redirect('engineer_signup')
        
            if password1 != password2:
                messages.add_message(request, messages.ERROR, 'Password does not match')
                return redirect('engineer_signup')
            
            user_obj = User.objects.create_user(username=username, email=email, password=password1)
            user_obj.set_password(password1)

            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()

            engineer_verification_email(email, auth_token, username)
            messages.success(request, 'Check your E-mail for verification Code!')
            return redirect('/engineer_token_send')
            
        
        except Exception as e:
            print(e)

    return render(request, "engineer/engineer_signup.html")

# Verification for Email
def engineer_verification_email(email,token, username):
    subject = 'Your account needs to be verified!'
    message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/engineer_verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

#Verify Email Token
def engineer_verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your Account is already Verified!')
                return redirect('/engineer_login')
            
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Hurray! Your Account has been Verified!')
            return redirect('/engineer_success')
        
        else:
            return redirect('engineer_error')
    except Exception as e:
        print(e)
        return redirect('/engineer_login')
    
# Forgot Password
def engineer_forgot_password(request):
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

                engineer_password_verify(email, auth_token, username)
                return redirect('engineer_update')    
            else:
                messages.error(request, 'User is not verified yet!')
                return redirect('engineer_forgot_password')
        
        else:
            messages.error(request, "Invalid Email! Please enter valid E-mail")
            return redirect('engineer_forgot_password')
        
    return render(request, 'engineer/engineer_forgot_password.html')

# Password Verify
def engineer_password_verify(email,token, username):
    subject = 'Request for Password Change!'
    message = f'Hi {username}! , Please use this link to reset your password: http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Reset Password 
def engineer_change_password(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.reset_password = True
            profile_obj.save()
            messages.success(request, 'Email Verified! Now you can change your Password.')
            return redirect('engineer_reset_password')
        else:
            return redirect('engineer_error')
    except Exception as e:
        print(e)

    return redirect('engineer_error')

# Reset Password
def engineer_reset_password(request):
    email = request.session['email']

    if request.method == 'POST':
        try:
            if Profile.objects.filter(reset_password=True):

                password = request.POST.get('password1')
                password1 = request.POST.get('password2')
                
                if len(password) < 8:
                    messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                    return redirect('engineer_reset_password')

                if password != password1:
                    messages.add_message(request, messages.ERROR, 'Password does not match')
                    return redirect('engineer_reset_password')

                user = User.objects.filter(email=email).first()
                user.set_password(password1)
                user.save()

                messages.success(request, 'Password Changed Successfully!')
                return redirect('engineer_login')
            
            else:
                messages.error(request, 'Email not verified yet!')
        except:
                messages.error(request, 'Update Error')
                return redirect('engineer_error')
        
    return render(request, 'engineer/engineer_reset_password.html')

# Success Template view
def engineer_success(request):
    return render(request, "engineer/engineer_success.html")

# token_send Template view
def engineer_token_send(request):
    return render(request, "engineer/engineer_token_send.html")

# Update Password
def engineer_update(request):
    return render(request, "engineer/engineer_update.html")

# Error Page
def engineer_error(request):
    return render(request, "engineer/engineer_error.html")

def Engineer_Log_Reg_Tem(request):
    return render(request, "engineer/engineer_log_reg.html")
