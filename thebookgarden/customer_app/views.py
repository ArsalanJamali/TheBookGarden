from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .forms import Register_User_Form,LoginForm
from django.urls import reverse_lazy
# Create your views here.

class SignUpView(CreateView,):
    template_name='accounts/register.html'
    model=get_user_model()
    form_class=Register_User_Form
    success_url=reverse_lazy('index')

class SignInView(LoginView):
    template_name='accounts/login.html'
    form_class=LoginForm



