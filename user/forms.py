from django.contrib.auth.models import User
from django import forms
from task.forms import StyledFormMixin
from django.contrib.auth.forms import PasswordChangeForm


class EditProfileFormModel(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
    
    profile_img = forms.ImageField(required=False,label='Image') 
    phone_number = forms.CharField(widget = forms.Textarea,required=False, label= 'phone_number')

    def __init__(self, *args, **kwargs):
       self.user_profile = kwargs.pop('user_profile',None)
       super().__init__(*args, **kwargs)

       if self.user_profile:
           self.fields['phone_number'].initial = self.user_profile.phone_number
           self.fields['profile_img'].initial = self.user_profile.profile_img

    def save(self, commit = True):
        user = super().save(commit)

        if self.user_profile:
            self.user_profile.phone_number = self.cleaned_data.get('phone_number')
            self.user_profile.profile_img = self.cleaned_data.get('profile_img')

            if commit:
                self.user_profile.save()

        if commit:
            user.save()
        return user
    
class CustomPasswordChange(StyledFormMixin,PasswordChangeForm):
    pass