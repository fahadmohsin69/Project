from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='ContactMessage'
        ordering = ['created_at']
    
    def __str__(self):
        return str(self.first_name)

class UserMaster(models.Model):
    email = models.EmailField(max_length = 50)
    password = models.CharField(max_length = 50)
    otp = models.IntegerField()
    role =  models.CharField(max_length = 50)
    is_active =  models.BooleanField(default = True)
    is_verified = models.BooleanField(default = False)
    is_created = models.DateTimeField(auto_now_add = True)
    is_update = models.DateTimeField(auto_now_add = True)

class Engineer(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    contact = models.CharField(max_length = 50)
    engineer_no = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    address = models.CharField(max_length = 150)
    dob = models.CharField(max_length = 50)
    gender = models.CharField(max_length = 50)
    profile_pic = models.ImageField(upload_to = "app1/img/Engineer")
    degree = models.CharField(max_length = 50)
    institue = models.CharField(max_length = 100)
    
    
class User(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    contact = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    address = models.CharField(max_length = 150)
    dob = models.CharField(max_length = 50)
    gender = models.CharField(max_length = 50)
    profile_pic = models.ImageField(upload_to = "app1/img/User")    


#For Email Verification
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reset_password = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    