from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from task.forms import StyledFormMixin
import re
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm

class RegistrationForm(StyledFormMixin,UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_checking = User.objects.filter(email = email).exists()

        if email_checking:
            raise forms.ValidationError("Email already exists")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append("Password must be at least 8 character long")
        if not re.search(r'[a-z]',password1):
            errors.append("Password must have a small character")
        if not re.search(r'[A-Z]',password1):
            errors.append("Password must have a capital character")
        if not re.search(r'[@#$&=+!^*]',password1):
            errors.append("Password must have a special character")
        if errors:
            raise forms.ValidationError(errors)
        return password1
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Password are not same!')


class LogInForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass

class CustomSetPasswordForm(StyledFormMixin,SetPasswordForm):
    pass