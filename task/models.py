from django.db import models


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

    def __str__(self):
        return self.name
    
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ManyToManyField(Event,related_name='participant')

    def __str__(self):
        return self.name
