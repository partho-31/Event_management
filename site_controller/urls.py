from django.urls import path
from .views import create_groups,assign_role,Admin_dashboard

urlpatterns = [
    path('create_groups/',create_groups,name='create_groups'),
    path('assign_role/<int:id>/',assign_role,name='assign_role'),
    path('admin_dashboard/',Admin_dashboard.as_view(),name= 'admin_dashboard'),

]
