from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ContactMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, decorators

from .models import userProfile
from .models import engineerProfile, engineerDetails
from .forms import *

#Email Authentication 
import uuid
from django.conf import settings
from django.core.mail import send_mail

############################ Home Views #############################################

from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


############################ Create your views here ##################################

def IndexPage(request):
    return render(request,'main/index.html')

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

def logoutUser(request):
    logout(request)
    return redirect('index')

########### Login and SignUp Views for User ###########

def user_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('home')
         
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)

            profile_obj = userProfile.objects.filter(user = user).first()

            if user is not None:
                if profile_obj.is_verified:
                    userProfile.objects.update(reset_password=False)
                    auth_login(request,user)
                    return redirect('home')
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
    if request.user.is_authenticated:
        return redirect('home')

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

            profile_obj = userProfile.objects.create(user = user_obj, auth_token = auth_token)
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
    # message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/user_verify/{token}'
    message = f'Hi {username}! , Please use this link to verify your account http://letengineers.com/user_verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

#Verify Email Token
def user_verify(request, auth_token):
    try:
        profile_obj = userProfile.objects.filter(auth_token = auth_token).first()
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

            if userProfile.objects.filter(is_verified=True):

                data = User.objects.get(email = email)
                auth_token = str(uuid.uuid4())
                
                userProfile.objects.update(auth_token = auth_token)
            
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
    # message = f'Hi {username}! , Please use this link to reset your password: http://127.0.0.1:8000/change_password/{token}'
    message = f'Hi {username}! , Please use this link to reset your password: http://letengineers.com/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Reset Password 
def user_change_password(request, auth_token):
    try:
        profile_obj = userProfile.objects.filter(auth_token = auth_token).first()
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
            if userProfile.objects.filter(reset_password=True):

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

def engineer_profile(request):
    return render(request, "engineer/profile.html")

def engineer_details(request):
    return render(request, "engineer/engineer_details.html")

def add_engineer_details(request):
    try:
        profile = engineerProfile.objects.get(user=request.user)
    except engineerProfile.DoesNotExist:
        profile = engineerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        # Extract form data
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        cnic = request.POST['cnic']
        degree = request.POST['degree']
        degreeType = request.POST['degreetype']
        university = request.POST['university']
        passOut = request.POST['passoutyear']
        pecNo = request.POST['pecnumber']
        address = request.POST['address']
        country = request.POST['country']

        # Create EngineerDetails object
        engineer_details = engineerDetails(
            profile = profile,
            firstname = firstname,
            lastname = lastname,
            dob = dob,
            gender = gender,
            contact = contact,
            cnic = cnic,
            degree = degree,
            degreeType = degreeType,
            university = university,
            passOut = passOut,
            pecNo = pecNo,
            address = address,
            country = country,
        )
        engineer_details.save()

        # Redirect to profile page or any other desired page
        return redirect('engineer_profile')  # Replace 'profile' with your actual URL name

    return render(request, 'engineer_details.html')

# Login View
def engineer_login(request):
    try:
        
        if request.user.is_authenticated:
            return redirect('home')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)

            profile_obj = engineerProfile.objects.filter(user=user).first()

            if user is not None:
                if profile_obj.is_verified:
                    auth_login(request, user)
                    if engineerDetails.objects.filter(profile=profile_obj).exists():
                        return redirect('home')
                    else:
                        return redirect('engineer_details')
                else:
                    messages.error(request, 'You are not Verified! Please check your Email.')
            else:
                messages.error(request, 'Invalid Username or Password!')
    except:
        messages.error(request, 'An Error Occurred!')
        return redirect('/engineer_login')

    return render(request, "engineer/engineer_login.html")

# SignUp view
def engineer_signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    
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

            profile_obj = engineerProfile.objects.create(user = user_obj, auth_token = auth_token)
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
    # message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/engineer_verify/{token}'
    message = f'Hi {username}! , Please use this link to verify your account http://letengineers.com/engineer_verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

#Verify Email Token
def engineer_verify(request, auth_token):
    try:
        profile_obj = engineerProfile.objects.filter(auth_token = auth_token).first()
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

            if engineerProfile.objects.filter(is_verified=True):

                data = User.objects.get(email = email)
                auth_token = str(uuid.uuid4())
                
                engineerProfile.objects.update(auth_token = auth_token)
            
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
    # message = f'Hi {username}! , Please use this link to reset your password: http://127.0.0.1:8000/change_password/{token}'
    message = f'Hi {username}! , Please use this link to reset your password: http://letengineers.com/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Reset Password 
def engineer_change_password(request, auth_token):
    try:
        profile_obj = engineerProfile.objects.filter(auth_token = auth_token).first()
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
            if engineerProfile.objects.filter(reset_password=True):

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

############### Home Page Views ###############  
@login_required(login_url='index')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:6]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'home_pages/home.html', context)

@login_required(login_url='index')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'home_pages/room.html', context)

@login_required(login_url='index')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'home_pages/profile.html', context)


@login_required(login_url='index')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'home_pages/room_form.html', context)


@login_required(login_url='index')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'home_pages/room_form.html', context)


@login_required(login_url='index')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'home_pages/delete.html', {'obj': room})


@login_required(login_url='index')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'home_pages/delete.html', {'obj': message})


@login_required(login_url='index')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'home_pages/update-user.html', {'form': form})

@login_required(login_url='index')
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'home_pages/topics.html', {'topics': topics})
