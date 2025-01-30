from django import forms
from .models import Event,Category,Participant

class StyledFormMixin:
    
    def StyledWidget(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({      
                    'class' : 'border-2 w-full border-red-300 px-2 rounded-lg' ,
                    'placeholder' : f"Enter {field_name}"
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class' : 'border-2 border-red-300 w-full px-2 rounded-lg',
                    'placeholder' : f'Enter {field_name}'
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class' :'border-2 border-red-300 w-full px-2 rounded-lg',
                    'placeholder' : f'Enter {field_name}',
                    'rows' : 2
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : 'border-2 border-red-300 rounded-lg',
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : ' rounded-lg'
                })
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.StyledWidget()
        


class CategoryFormModel(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class EventFormModel(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields =  '__all__'
        widgets = {
            'deadline' : forms.SelectDateWidget,
            'category' : forms.Select(attrs={
                'class':'w-1/2 border-2 border-red-300 rounded-lg'
                })
        }

class ParticipantFormModel(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'event' : forms.CheckboxSelectMultiple,
        }
