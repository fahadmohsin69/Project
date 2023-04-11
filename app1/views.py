from django.shortcuts import render
# from .forms import ContactForm
from .models import ContactMessage

# Create your views here.
def IndexPage(request):
    return render(request,'main/main.html')

def contact_us(request):
    if request.method == 'POST':
        if request.method == 'POST':
            first_name = request.POST.get('first_name', '')
            print(first_name)
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            contact_message = ContactMessage(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
            contact_message.save()
            return render(request, 'main/main.html',{'success': True})
    else:
        return render(request, 'main/main.html',{'success': False})

############### Engineer Side ###############

def Engin_Log_Reg_Tem(request):
    return render(request, "engineer/engineer_log_reg.html")

############### User Side ###############

def User_Log_Reg_Tem(request):
    return render(request, "user/user_log_reg.html")