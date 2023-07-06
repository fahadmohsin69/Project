from functools import wraps
from django.http import HttpResponse, request
from django.urls import reverse

def login_required_alert(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            alert_message = "Please login first."
            user_login_url = reverse('index')
            return HttpResponse(f"<script>alert('{alert_message}'); window.location.href = '{user_login_url}';</script>")
            
        return view_func(request, *args, **kwargs)
    
    return wrapper
