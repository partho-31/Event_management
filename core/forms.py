from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User,Group,Permission
from task.forms import StyledFormMixin
import re

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
        
class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset = Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission',
    )
    class Meta:
        model = Group
        fields = ['name','permissions']
        widgets ={
            'name' : forms.TextInput(attrs={
                'class' : 'border-2 border-red-600 p-1 rounded-xl',
            })
        }

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label= "Select a role",
    )