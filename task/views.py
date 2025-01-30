from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q,Count
from .forms import CategoryFormModel,EventFormModel,ParticipantFormModel
from django.contrib import messages
from .models import Event,Category,Participant
from datetime import datetime


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
        form = EventFormModel(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Event added successfuly")
            return redirect('add_event')

    return render(request,'event_form.html',{"forms":form})


def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        return redirect('event_list')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('category_list')

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

def add_category(request):
    form = CategoryFormModel()

    if request.method == 'POST':
        form = CategoryFormModel(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category added successfuly")
            return redirect('add_category')
        
    return render(request,'category_form.html',{"forms":form})

def update_category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryFormModel(instance=category)

    if request.method == 'POST':
        form = CategoryFormModel(request.POST,instance = category)
        form.save()
        messages.success(request,"Updated successfuly")
        return redirect('update_category',id)
    
    return render(request,'category_form.html',{'forms': form})

def delete_category(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category_list')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('category_list')
   

def add_participant(request):
    form = ParticipantFormModel()

    if request.method == 'POST':
        form = ParticipantFormModel(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Participant added successfuly")
            return redirect('add_participant')
        
    return render(request,'participant_form.html',{"forms":form})


def update_participant(request,id):
    participant = Participant.objects.get(id=id)
    form = ParticipantFormModel(instance=participant)

    if request.method == 'POST':
        form = ParticipantFormModel(request.POST,instance = participant)
        form.save()
        messages.success(request,"Updated successfuly")
        return redirect('update_participant',id)
    
    return render(request,'participant_form.html',{'forms': form})

def delete_participant(request,id):
    if request.method == 'POST':
        participant = Participant.objects.get(id=id)
        participant.delete()
        return redirect('participant_list')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('participant_list')
   
def view_event(request):
    event_list = Event.objects.select_related('category').all()
    return render(request,'event.html',{'event_list': event_list})

def view_category(request):
    category_list = Category.objects.all()
    return render(request,'category.html',{'category_list' : category_list})

def view_participant(request):
    participants = Participant.objects.prefetch_related('event').all()
    return render(request,'participant.html',{'participants' : participants})

