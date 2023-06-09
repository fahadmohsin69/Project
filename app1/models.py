from django.db import models
from django.contrib.auth.models import User

# from .models import Profile


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ContactMessage'
        ordering = ['created_at']

    def __str__(self):
        return str(self.first_name)


class engineerDetails(models.Model):
    profile = models.OneToOneField('engineerProfile', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=25)
    cnic = models.CharField(max_length=15)
    degree = models.CharField(max_length=50)
    degreeType = models.CharField(max_length=50)
    university  = models.CharField(max_length=50)
    passOut = models.DateField()
    pecNo = models.CharField(max_length=50)
    #profile_pic = models.ImageField(upload_to="app1/img/Engineer")

    class Meta:
        db_table = 'engineerDetails'
        ordering = ['firstname']

    def __str__(self):
        return str(self.firstname)
    
class userDetails(models.Model):
    profile = models.OneToOneField('userProfile', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=25)

    class Meta:
        db_table = 'userDetails'
        ordering = ['firstname']

    def __str__(self):
        return str(self.firstname)

# For Email Verification
class engineerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reset_password = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'engineerProfile'
        ordering = ['created_at']

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reset_password = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'userProfile'
        ordering = ['created_at']


############## Home Page Models #################

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated =models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]