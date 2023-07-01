from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.IndexPage, name="index"),

    path("contact-us/", views.contact_us, name="contact_us"),

    ############### Main Pages ###############  

    path("home/", views.home, name="home"),
    
    ############### User Side ###############    

    path("user-log-reg/", views.User_Log_Reg_Tem, name="user_log_reg"),

    path("user_login/", views.user_login, name="user_login"),
    
    path("user_signup/", views.user_signup, name="user_signup"),
    
    path("user_success/", views.user_success, name="user_success"),

    path("user_update/", views.user_update, name="user_update"),

    path("user_forgot_password/", views.user_forgot_password, name="user_forgot_password"),

    path("user_reset_password/", views.user_reset_password, name="user_reset_password"),
    
    path("user_token_send/", views.user_token_send, name="user_token_send"),

    path('user_error', views.user_error, name='user_error'),

    path('user_verify/<auth_token>', views.user_verify, name='user_verify'),

    path('user_change_password/<auth_token>', views.user_change_password, name='user_change_password'),

    
    ############### Engineer Side ###############

    path("engineer-log-reg/", views.Engineer_Log_Reg_Tem, name="engineer_log_reg"),
    
    path("engineer_login/", views.engineer_login, name="engineer_login"),
    
    path("engineer_signup/", views.engineer_signup, name="engineer_signup"),
    
    path("engineer_success/", views.engineer_success, name="engineer_success"),

    path("engineer_update/", views.engineer_update, name="engineer_update"),

    path("engineer_forgot_password/", views.engineer_forgot_password, name="engineer_forgot_password"),

    path("engineer_reset_password/", views.engineer_reset_password, name="engineer_reset_password"),
    
    path("engineer_token_send/", views.engineer_token_send, name="engineer_token_send"),

    path('engineer_error', views.engineer_error, name='engineer_error'),

    path('engineer_verify/<auth_token>', views.engineer_verify, name='engineer_verify'),

    path('engineer_change_password/<auth_token>', views.engineer_change_password, name='engineer_change_password'),

    path('engineer_details', views.engineer_details, name='engineer_details'),

    path('engineer_profile', views.engineer_profile, name='engineer_profile'),

    path('add_engineer_details', views.add_engineer_details, name='add_engineer_details'),

    ######################### Home Page URLS ####################################
    
    path('room/<str:pk>/', views.room, name="room"),

    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),

    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),

    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
]
