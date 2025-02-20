from django.urls import path
from .views import main_page,sign_in,sign_up,activate_acc,sign_out,PasswordReset,PasswordResetConfirm

urlpatterns = [
    path('',main_page,name='front_page'),
    path('sign_in/',sign_in,name='sign_in'),
    path('sign_up/',sign_up,name='sign_up'),
    path('activate/<int:user_id>/<str:token>/',activate_acc),
    path('sign_out/',sign_out,name='sign_out'),
    path('reset_password/',PasswordReset.as_view(template_name = 'password_reset_form.html'),name= 'password_reset'),
    path('reset_password/<uidb64>/<token>/',PasswordResetConfirm.as_view(template_name = 'password_reset_form.html'),name= 'password_reset_confirm')
]


