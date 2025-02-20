from django.db import models
from django.contrib.auth.models import User


class User_profile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE,related_name='user_profile',primary_key=True)
    profile_img = models.ImageField(upload_to= 'profile_img',default='profile_img/default.jpg',blank=True)
    phone_number = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.first_name}"
