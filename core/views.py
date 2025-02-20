from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegistrationForm,LogInForm,CustomPasswordResetForm,CustomSetPasswordForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from task.models import Event,Category
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.urls import reverse_lazy

def is_admin(user):
    return user.groups.filter(name = 'Admin').exists()

def is_manager(user):
    return user.groups.filter(name= 'Manager').exists()


def main_page(request):
    return render(request,'home.html')

def sign_in(request):
    form = LogInForm()
    if request.method == 'POST':
        form = LogInForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Manager').exists():
                return redirect('organizer_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
    return render(request,'login_form.html',{'forms':form})

def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            
            user.save()
            messages.success(request,"A message is send to your email please click on the link to active account")
            return redirect('sign_in')
    return render(request,'registration_form.html',{'forms':form})


def activate_acc(request,user_id,token):
    user = User.objects.get(id = user_id) 
    if default_token_generator.check_token(user,token):
        user.is_active = True
        user.save() 
        return redirect('sign_in')
    else:
        return HttpResponse("Invalid id or token")
    

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign_in')


@login_required
@user_passes_test(is_manager,login_url= 'front_page')
def organizer_dashboard(request):
    type = request.GET.get('type',"")

    events = ""
    category = ""

    if type == 'category':
        category = Category.objects.all()
    else :
        events = Event.objects.all()
    return render(request,'organizer.html',{'events': events,'categorys': category})



class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    html_email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context 

    def form_valid(self, form):
        messages.success(self.request,"A password resent email is sent to your email.Please check your inbox.")
        return super().form_valid(form)
    
class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('sign_in')

    def form_valid(self, form):
        messages.success(self.request,"Password reset succesful!")
        return super().form_valid(form)