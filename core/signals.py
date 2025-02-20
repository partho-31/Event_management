from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.conf import settings
from user.models import User_profile

@receiver(post_save,sender = User)
def activation_link(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        recipent_list = [instance.email]
        send_mail(
            'Activation Link',
            f'Hi {instance.username}\nPlease click on the link to active your account\n\n{settings.FRONTEND_URL}/activate/{instance.id}/{token}/\n\nThank you!',
            'parthokumarmondal90@gmail.com',
            recipent_list,     
        )
    
@receiver(post_save,sender = User)
def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group,created = Group.objects.get_or_create(name = 'User')
        instance.groups.add(user_group)
        instance.save()
    
@receiver(post_save,sender = User)
def create_profile_after_user(sender,instance,created,**kwargs):
    if created:
        User_profile.objects.create(user = instance)
    