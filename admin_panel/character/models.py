from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.
class character(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='assets/character_images/', null=True, blank=True)
    avatar=models.ImageField(upload_to='assets/character_avatars/' ,null=True, blank=True)
    description=models.CharField(max_length=600)
    goal=models.CharField(max_length=250)
    strategy = models.JSONField(default=list, blank=True)
    symbols=models.CharField(max_length=250,blank=True,default="")
    slogan=models.CharField(max_length=250,blank=True,default="")
    weekness=models.CharField(max_length=250)
    roal=models.CharField(max_length=250)
    personality=models.CharField(max_length=250)
    age=models.PositiveIntegerField(default=0)
    sex=models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


@receiver(post_delete, sender=character)
def delete_image_on_character_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.avatar:
        instance.avatar.delete(save=False)
