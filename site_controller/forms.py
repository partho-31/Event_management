from django import forms
from django.contrib.auth.models import Group,Permission
from task.forms import StyledFormMixin


        
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

class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label= "Select a role",
    )