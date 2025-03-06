from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import CreateGroupForm,AssignRoleForm
from core.views import is_admin
from django.contrib.auth.models import User,Group
from task.models import Event
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


class Admin_dashboard(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        type = self.request.GET.get('type')
        if type == 'events':
            events = Event.objects.select_related('category').all()
            context['events'] = events
        elif type == 'groups':
            groups = Group.objects.prefetch_related('permissions').all()
            context['groups'] = groups
        else:
            user = User.objects.all()
            context['users'] = user
        return context


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