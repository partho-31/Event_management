from django.shortcuts import render,redirect
from django.db.models import Q
from .forms import CategoryFormModel,EventFormModel
from django.contrib import messages
from .models import Event,Category
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from core.views import is_manager,is_admin
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def search(request):
    text = request.GET.get('text'," ")
    events = Event.objects.filter(Q(name__icontains=text) | Q(location__icontains=text)) 
    return render(request,'search.html',{'forms' : events})

@login_required
@user_passes_test(is_manager,login_url='no_permission')
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
@user_passes_test(is_manager,login_url='no_permission')
def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        return redirect('organizer_dashboard')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('organizer_dashboard')


class Update_event(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Event
    form_class = EventFormModel
    context_object_name = 'forms'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forms"] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        event = self.get_object()
        form = EventFormModel(request.POST,instance = event)

        if form.is_valid():
            form.save()
            messages.success(request,"Event updated successfuly")
            return redirect('update_event',event.id)
        return redirect('update_event',event.id)
        
    def test_func(self):
        return is_manager(self.request.user)



@login_required
@user_passes_test(is_manager,login_url='no_permission')
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
@user_passes_test(is_manager,login_url='no_permission')
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
@user_passes_test(is_manager,login_url='no_permission')
def delete_category(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('organizer_dashboard')
    else:
        messages.error(request,"Something went wrong!")
        return redirect('organizer_dashboard')
 

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


def No_permission(request):
    return render(request,'no_permission.html')
