from django.urls import path, include
from .import views
urlpatterns = [
    path("", views.IndexPage, name="index"),
    path("contact-us/", views.contact_us, name="contact_us"),
    
    ############### Engineer Side ###############
    path("engin-log-reg/", views.Engin_Log_Reg_Tem, name="engin_log_reg"),
    
    ############### User Side ###############
    path("user-log-reg/", views.User_Log_Reg_Tem, name="engin_log_reg"),
]
