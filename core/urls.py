from django.urls import path
from .views import main_page,sign_in,sign_up,activate_acc,create_groups,assign_role,sign_out,organizer_dashboard

urlpatterns = [
    path('',main_page,name='front_page'),
    path('sign_in/',sign_in,name='sign_in'),
    path('sign_up/',sign_up,name='sign_up'),
    path('activate/<int:user_id>/<str:token>/',activate_acc),
    path('create_groups/',create_groups,name='create_groups'),
    path('assign_role/<int:id>/',assign_role,name='assign_role'),
    path('sign_out/',sign_out,name='sign_out'),
]


