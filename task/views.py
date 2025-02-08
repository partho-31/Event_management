from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q,Count
from .forms import CategoryFormModel,EventFormModel
from django.contrib import messages
from .models import Event,Category
from datetime import datetime
from django.contrib.auth.models import User,Group,Permission
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from core.views import is_admin,is_manager

@login_required
def dashboard(request): 
    type = request.GET.get('type',"")

    upcoming = ""
    past_event= ""
    total_event = ""
    today = ""

    if type == 'upcoming':
        upcoming = Event.objects.filter(deadline__gt = datetime.now())
    elif type == 'past':
        past_event = Event.objects.filter(deadline__lt = datetime.now())
    elif type == 'total':
        total_event = Event.objects.select_related('category').all()
    else:
        today = Event.objects.filter(deadline = datetime.today())

    count_event = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id', filter=Q(deadline__gt= datetime.now())),
        past_event = Count('id', filter=Q(deadline__lt= datetime.now())),
    )
    count_category = Category.objects.aggregate(
        total = Count('id'),
    )
    return render(request,"dashboard.html",{
        'count_e' : count_event,
        'count_c' : count_category,
        'upcoming' : upcoming,
        'past_event' : past_event,
        'total_event' : total_event,
        'today' : today,
        })

def search(request):
    text = request.GET.get('text'," ")
    events = Event.objects.filter(Q(name__icontains=text) | Q(location__icontains=text)) 
    return render(request,'search.html',{'forms' : events})

def add_event(request):
    form = EventFormModel()
    if request.method == 'POST':
        form = EventFormModel(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Event added successfuly")
            return redirect('add_event')
    return render(request,'event_form.html',{"forms":form})

@login_required
@user_passes_test(is_manager,login_url='front_page')
def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        return redirect('event_list')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('event_list')

@login_required
@user_passes_test(is_manager,login_url='front_page')
def update_event(request,id):
    event = Event.objects.get(id=id)
    event_form = EventFormModel(instance=event)

    if request.method == 'POST':
        event_form = EventFormModel(request.POST,instance = event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request,"Updated successfuly")
            return redirect('update_event',id)

    return render(request,'event_form.html',{'forms':event_form})

@login_required
@user_passes_test(is_manager,login_url='front_page')
def add_category(request):
    form = CategoryFormModel()
    if request.method == 'POST':
        form = CategoryFormModel(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category added successfuly")
            return redirect('add_category')    
    return render(request,'category_form.html',{"forms":form})

@login_required
@user_passes_test(is_manager,login_url='front_page')
def update_category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryFormModel(instance=category)

    if request.method == 'POST':
        form = CategoryFormModel(request.POST,instance = category)
        form.save()
        messages.success(request,"Updated successfuly")
        return redirect('update_category',id)
    
    return render(request,'category_form.html',{'forms': form})

@login_required
@user_passes_test(is_manager,login_url='front_page')
def delete_category(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category_list')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('category_list')
 
   
def view_event(request):
    event_list = Event.objects.select_related('category').all()
    return render(request,'event.html',{'event_list': event_list})

def view_category(request):
    category_list = Category.objects.all()
    return render(request,'category.html',{'category_list' : category_list})

@login_required
@user_passes_test(is_admin,login_url= 'front_page')
def admin_dashboard(request):
    type = request.GET.get('type',"")

    events = ""
    groups = ""
    user = ""

    if type == 'events':
        events = Event.objects.select_related('category').all()
    elif type == 'groups':
        groups = Group.objects.prefetch_related('permissions').all()
    else:
        user = User.objects.all()
    return render(request,'admin_dashboard.html',{'users':user,'events': events,'groups': groups})

def rsvp(request,id):
    event = Event.objects.get(id = id)
    if event.participants.filter(id= request.user.id).exists():
        messages.error(request,f'You have all ready take place in { event.name }!')
        return render(request,'confirmation.html')
    else:
        user = request.user
        participant_mail = [user.email]
        event.participants.add(user.id)
        send_mail(
            "Inviation Paper",
            f"Hi! {user.username}\nYou have succesfuly registered for {event.name} .Don't forget to check deadlines.We hope you will be on time\n\nThank you!",
            'parthokumarmondal90@gmail.com',
            participant_mail,
        )

        messages.success(request,"You have succesfuly take place in this event!")
        return render(request,'confirmation.html')
    
def event_details(request,id):
    event = Event.objects.get(id = id)
    return render(request,'event_details.html',{'event' : event})