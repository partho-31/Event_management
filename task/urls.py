from django.contrib import admin
from django.urls import path
from .views import *
from core.views import organizer_dashboard

urlpatterns = [
   
    path('add_event/',add_event,name="add_event"),
    path('add_category/',add_category,name="add_category"),  
    path('delete_event/<int:id>/',delete_event,name='delete_event'),
    path('update_event/<int:id>/',Update_event.as_view(template_name = 'event_form.html'),name='update_event'),
    path('delete_category/<int:id>/',delete_category,name='delete_category'),
    path('update_category/<int:id>/',update_category,name='update_category'),
    path('search/',search,name='search'),
    path('organizer_dashboard/',organizer_dashboard,name='organizer_dashboard'),
    path('add_to_rsvp/<int:id>/',rsvp,name='add_to_rsvp'),
    
]