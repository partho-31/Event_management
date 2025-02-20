from django.shortcuts import render,redirect
from task.models import Event,Category
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q,Count
from django.views.generic import TemplateView,ListView,DetailView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileFormModel,CustomPasswordChange
from django.urls import reverse_lazy
from .models import User_profile
from django.contrib.auth.views import PasswordChangeView


class User_dashboard(LoginRequiredMixin,TemplateView):

    def get_context_data(self, **kwargs):
        type = self.request.GET.get('type')
        context = super().get_context_data(**kwargs)

        count_event = Event.objects.aggregate(
            total = Count('id'),
            upcoming = Count('id', filter=Q(deadline__gt= datetime.now())),
            past_event = Count('id', filter=Q(deadline__lt= datetime.now())),
        )
        count_category = Category.objects.aggregate(
            total = Count('id'),
        )

        context['count_event'] = count_event
        context['count_category'] = count_category

        if type == 'upcoming':
            upcoming = Event.objects.filter(deadline__gt = datetime.now())
            context['upcoming'] = upcoming
        elif type == 'past':
            past_event = Event.objects.filter(deadline__lt = datetime.now())
            context['past_event'] = past_event
        elif type == 'total':
            total_event = Event.objects.select_related('category').all()
            context['total_event'] = total_event
        else:
            today = Event.objects.filter(deadline = datetime.today())
            context['today'] = today

        return context
    

class Event_details(LoginRequiredMixin,DetailView):
    model = Event
    context_object_name = 'event'
    pk_url_kwarg = 'id'


class View_event(LoginRequiredMixin,ListView):
    model = Event
    template_name = 'event.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset
    

def view_category(request):
    category_list = Category.objects.all()
    return render(request,'category.html',{'category_list' : category_list})

def profile_view(request):
    user = request.user
    return render(request,'profile.html',{'user': user})


class Edit_profile(LoginRequiredMixin,UpdateView):
    model = User
    form_class = EditProfileFormModel
    context_object_name = 'form'
    success_url = reverse_lazy('profile_view')
    
    def get_object(self):
        return self.request.user 
    
    def get_form_kwargs(self):
        Kwargs = super().get_form_kwargs()
        Kwargs['user_profile'] = User_profile.objects.get(user = self.request.user)
        return Kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = User_profile.objects.get(user = self.request.user)
        context['form'] = self.form_class(instance = self.request.user , user_profile = user_profile)
        return context
   
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile_view')
    
class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChange
    success_url = reverse_lazy('profile_view')