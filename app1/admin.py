from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name","email","subject","message","created_at")

