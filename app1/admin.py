from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(engineerProfile)
# admin.site.register(userProfile)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name","email","subject","message","created_at")

@admin.register(engineerProfile)
class engineerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "auth_token","is_verified","created_at","reset_password")

@admin.register(userProfile)
class userProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "auth_token","is_verified","created_at","reset_password")    

    
@admin.register(engineerDetails)
class engineerDetailsAdmin(admin.ModelAdmin):
    list_display = ("profile", "firstname","lastname","dob","gender","contact","cnic","degree",
    "degreeType","university","passOut","pecNo","address","country")

