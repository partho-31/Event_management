from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegistrationForm,LogInForm,CreateGroupForm,AssignRoleForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from task.models import Event,Category



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

@login_required
@user_passes_test(is_admin,login_url='no_permission') 
def create_groups(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_groups')
    return render(request,'create_group.html',{'forms' : form})

@login_required
@user_passes_test(is_admin,login_url='no_permission')
def assign_role(request,id):
    user = User.objects.get(id=id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(data)
            user.save()
            return redirect('admin_dashboard')
    return render(request,'assign_role.html',{'forms': form})

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

