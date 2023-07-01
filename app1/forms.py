from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

############## Home Page Forms################
from django.forms import ModelForm
from .models import Room


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','password']
        
