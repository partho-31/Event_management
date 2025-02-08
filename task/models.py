from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50)
    deadline = models.DateField()
    category = models.ForeignKey(Category,on_delete= models.CASCADE,related_name='event')
    pictures = models.ImageField(upload_to='task_pictures' ,blank= True,null=True)
    participants = models.ManyToManyField(User,related_name='rsvp_event')

    def __str__(self):
        return self.name
    

