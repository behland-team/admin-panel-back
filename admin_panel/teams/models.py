from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.
class TeamMember(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='assets/team_photos/')
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.position}"
    
@receiver(post_delete, sender=TeamMember)
def delete_photo_on_team_member_delete(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)