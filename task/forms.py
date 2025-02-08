from django import forms
from .models import Event,Category

class StyledFormMixin:  
    def StyledWidget(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({      
                    'class' : 'py-2 px-3 w-full outline-none font-mono text-white placeholder-slate-300 placeholder-opacity-50 bg-slate-400 bg-opacity-20 rounded-lg ' ,
                    'placeholder' : f"Enter {field_name}"
                }) 
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class' : 'py-2 px-3 w-full outline-none font-mono text-white placeholder-slate-300 placeholder-opacity-50 bg-slate-400 bg-opacity-20 rounded-lg ',
                    'placeholder' : f'Enter {field_name}'
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class' :'py-2 px-3 w-full outline-none font-mono text-white placeholder-slate-300 placeholder-opacity-50 bg-slate-400 bg-opacity-20 rounded-lg ',
                    'placeholder' : f'Enter {field_name}',
                    'rows' : 2
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : 'py-2 px-3 outline-none font-mono text-white placeholder-slate-300 placeholder-opacity-50 bg-slate-400 bg-opacity-20 rounded-lg ',
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : 'm-2 rounded-lg'
                })
            elif isinstance(field.widget,forms.PasswordInput):
                field.widget.attrs.update({
                    'class' : 'py-2 px-3 w-full outline-none font-mono text-white placeholder-slate-300 placeholder-opacity-50 bg-slate-400 bg-opacity-20 rounded-lg ' ,
                    'placeholder' : f"{field.label}"
                })
            elif isinstance(field.widget,forms.ClearableFileInput):
                field.widget.attrs.update({
                    'class' : 'border-2 m-2 px-2 rounded-lg'
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
            'category' : forms.RadioSelect(attrs={
                'class':'border-2 m-2 px-2 rounded-lg',
                
                }),
            'participants' : forms.CheckboxSelectMultiple
        }


