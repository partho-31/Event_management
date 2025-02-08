from django.contrib import admin
from django.urls import path
from .views import *
from core.views import organizer_dashboard

urlpatterns = [
    path('dashboard/',dashboard,name="home"),
    path('add_event/',add_event,name="add_event"),
    path('add_category/',add_category,name="add_category"),
    path('view_event/',view_event,name="event_list"),
    path('view_category/',view_category,name="category_list"),
    path('delete_event/<int:id>/',delete_event,name='delete_event'),
    path('update_event/<int:id>/',update_event,name='update_event'),
    path('delete_category/<int:id>/',delete_category,name='delete_category'),
    path('update_category/<int:id>/',update_category,name='update_category'),
    path('search/',search,name='search'),
    path('admin_dashboard/',admin_dashboard,name= 'admin_dashboard'),
    path('organizer_dashboard/',organizer_dashboard,name='organizer_dashboard'),
    path('add_to_rsvp/<int:id>/',rsvp,name='add_to_rsvp'),
    path('event_details/<int:id>/',event_details,name='event_details'), 
]