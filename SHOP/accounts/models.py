from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile/',default='img_3.jpg',null=True,blank=True)

    def __str__(self):
        return self.user.username

def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()



post_save.connect(save_profile_user,sender=User)