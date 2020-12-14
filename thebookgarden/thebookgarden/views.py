from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

class HomePage(TemplateView):
    template_name='index.html'

def ContactUsView(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        subject='Contact us request from {}'.format(name)
        message=request.POST['message']
        email_body="Name: {}\nMessage: {}\nMail to Reply: {}\n".format(name,message,email)
        try:
            send_mail(
                subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except:
            messages.error(request,_("Due to some reason response wasn't recorded kindly send it again"))
        else:
            messages.success(request,_("Your response has been recorded we will get back to you soon"))
    
    return render(request,"contact-us.html")

class AboutUsView(TemplateView):
    template_name='about-us.html'

