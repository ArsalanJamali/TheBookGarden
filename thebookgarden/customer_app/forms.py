from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.utils.translation import ugettext_lazy as _

class Register_User_Form(UserCreationForm):

    class Meta:
        model=get_user_model()
        fields=('username','email','password1','password2')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label='Username'
        self.fields['username'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your username','data-content':self.fields['username'].help_text,'data-placement':'top','data-container':'body'}
        self.fields['email'].label="Email"
        self.fields['email'].widget.attrs={'class':'input100','placeholder':'Type your email'}
        self.fields['password1'].label='Password'
        self.fields['password1'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your password','data-placement':'top','data-container':'body'}
        self.fields['password2'].label='Confirm Password'
        self.fields['password2'].widget.attrs={'class':'input100','placeholder':'Type your password'}
        
    def clean_email(self):
        email=self.cleaned_data['email']
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('User with this email address already exists.'))
        return email.lower()

    def clean_username(self):
        username=self.cleaned_data['username']
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_('User with this username already exists'))
        return username.lower()


class LoginForm(AuthenticationForm):
    username=UsernameField(
        label='Username',
        widget=forms.TextInput(attrs={'class':'input100','placeholder':'Type your username'})
    )
    password=forms.CharField(
        label="Password",
		strip=False,
		widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Type your password'}),
    )


 

