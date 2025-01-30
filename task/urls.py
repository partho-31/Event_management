from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',dashboard,name="home"),
    path('add_event/',add_event,name="add_event"),
    path('add_category/',add_category,name="add_category"),
    path('add_participant/',add_participant,name ="add_participant"),
    path('view_event/',view_event,name="event_list"),
    path('view_category/',view_category,name="category_list"),
    path('view_participant/',view_participant,name="participant_list"),
    path('delete_event/<int:id>/',delete_event,name='delete_event'),
    path('update_event/<int:id>',update_event,name='update_event'),
    path('delete_category/<int:id>/',delete_category,name='delete_category'),
    path('update_category/<int:id>',update_category,name='update_category'),
    path('delete_participant/<int:id>/',delete_participant,name='delete_participant'),
    path('update_participant/<int:id>',update_participant,name='update_participant'),
    path('search/',search,name='search')
   
    
]