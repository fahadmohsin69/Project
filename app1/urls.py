from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.IndexPage, name="index"),

    path("home_page/", views.home_page, name="home_page"),

    path("contact-us/", views.contact_us, name="contact_us"),
    
    ############### Engineer Side ###############
    path("engin-log-reg/", views.Engin_Log_Reg_Tem, name="engin_log_reg"),
    
    ############### User Side ###############
    path("user-log-reg/", views.User_Log_Reg_Tem, name="user_log_reg"),

    path("login/", views.login, name="login"),
    
    path("signup/", views.signup, name="signup"),
    
    path("success/", views.success, name="success"),

    path("update/", views.update, name="update"),

    path("forgot_password/", views.forgot_password, name="forgot_password"),

    path("reset_password/", views.reset_password, name="reset_password"),
    
    path("token_send/", views.token_send, name="token_send"),

    path('error', views.error, name='error'),

    path('verify/<auth_token>', views.verify, name='verify'),

    path('change_password/<auth_token>', views.change_password, name='change_password'),
]
