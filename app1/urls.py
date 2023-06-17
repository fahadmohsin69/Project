from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.IndexPage, name="index"),
    path("home_page/", views.home_page, name="home_page"),

    path("contact-us/", views.contact_us, name="contact_us"),
    
    ############### Engineer Side ###############
    path("engin-log-reg/", views.Engin_Log_Reg_Tem, name="engin_log_reg"),
    
    ############### User Side ###############
    path("user-log-reg/", views.User_Log_Reg_Tem, name="engin_log_reg"),

    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("success/", views.success, name="success"),
    path("token_send/", views.token_send, name="token_send"),
]
