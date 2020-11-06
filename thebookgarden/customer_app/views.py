from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .forms import Register_User_Form,LoginForm,CustomPasswordResetForm,CustomPasswordConfirmForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate,login
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView

def ActivateUserAccountView(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=get_user_model().objects.get(pk=uid)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,_('Congratulations! Your Account Has been activated now you can proceed to logging yourself in..'))
        return redirect('customer_app:login')
    else:
        raise Http404(_('Activation Link is Invalid'))  


def SendAccountActivationLinkView(request,uid64):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=get_user_model().objects.get(pk=uid)
    except:
        user=None
    if user is not None:
        current_site=get_current_site(request)
        mail_subject='Activate Your Account'
        mail_message=render_to_string('accounts/account_activate.html',{
              'user':user,
              'domain':current_site.domain,
              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
              'token':account_activation_token.make_token(user)  
            
            })

        mail_to_send=EmailMessage(
                mail_subject,
                mail_message,
                to=[user.email]
            )
        mail_to_send.send(fail_silently=True)
        messages.success(request,_('Activation Link Has been sent kindly verify your email inorder to activate your account'))            
        return redirect('customer_app:login')
    else:
        raise Http404()


class SignUpView(CreateView):
    template_name='accounts/register.html'
    model=get_user_model()
    form_class=Register_User_Form
    success_url=reverse_lazy('index')

    def post(self,request,*args, **kwargs):
        form=Register_User_Form(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            mail_subject='Activate Your Account'
            mail_message=render_to_string('accounts/account_activate.html',{
              'user':user,
              'domain':current_site.domain,
              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
              'token':account_activation_token.make_token(user)  
            
            })

            mail_to_send=EmailMessage(
                mail_subject,
                mail_message,
                to=[form.cleaned_data['email']]
            )

            mail_to_send.send(fail_silently=True)
            messages.success(request,_('Your Account is successfully created kindly verify your email inorder to activate your account'))
            return redirect('customer_app:register')
        else:
            return render(request,self.template_name,{'form':form})    



class SignInView(LoginView):
    template_name='accounts/login.html'
    authentication_form=LoginForm

    def post(self,request,*args, **kwargs):
        form=LoginForm(data=request.POST)
        
        if form.is_valid():
            user=authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                try:
                    return redirect(self.request.GET.get('next'))
                except:    
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                try:
                    user=get_user_model().objects.get(
                                                    Q(email__iexact=form.cleaned_data['username']) | 
                                                    Q(username__iexact=form.cleaned_data['username']) 
                                                    )
                except:
                    form.add_error('username',ValidationError(_('Invalid Credentials')))
                    return render(request,self.template_name,{'form':form})
                else:
                    if not user.is_active:
                        return render(request,self.template_name,{'form':form,
                                                                 'have_link':True,
                                                                 'uid':urlsafe_base64_encode(force_bytes(user.pk))
                                                                 })
                    else:
                        form.add_error('password',ValidationError(_('Invalid Credentials')))
                        return render(request,self.template_name,{'form':form})
        else:
            return render(request,self.template_name,{'form':form})    

class PasswordResetClassView(PasswordResetView):
    template_name='Password_reset/password_reset_form.html'
    email_template_name='Password_reset/password_reset_email.html'
    subject_template_name='Password_reset/password_reset_subject.txt'
    success_url=reverse_lazy('customer_app:password_reset_done')
    form_class=CustomPasswordResetForm

class PasswordConfirmClassView(PasswordResetConfirmView):
    template_name='Password_reset/password_reset_confirm.html'
    success_url=reverse_lazy('customer_app:password_reset_confirm_done')
    form_class=CustomPasswordConfirmForm


