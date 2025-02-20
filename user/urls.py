from django.urls import path 
from .views import User_dashboard,View_event,view_category,Event_details,profile_view,Edit_profile,PasswordChange

urlpatterns = [
    path('dashboard/',User_dashboard.as_view(template_name = 'dashboard.html'),name="home"),
    path('profile/',profile_view,name="profile_view"),
    path('view_event/',View_event.as_view(),name="event_list"),
    path('view_category/',view_category,name="category_list"),
    path('event_details/<int:id>/',Event_details.as_view(template_name = 'event_details.html'),name='event_details'),
    path('edit_profile/',Edit_profile.as_view(template_name = 'edit_profile.html'),name='edit_profile'), 
    path('change_password/',PasswordChange.as_view(template_name = 'password_change.html'),name = 'change_password'),

]
