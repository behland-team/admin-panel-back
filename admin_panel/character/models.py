from django.db import models

# Create your models here.
class character(models.Model):
    name = models.CharField(max_length=100)
    # image
    # avatar
    description=models.CharField(max_length=600)
    goal=models.CharField(max_length=250)
    strategy=models.CharField(max_length=250)
    roal=models.CharField(max_length=250)
    personality=models.CharField(max_length=250)
    age=models.PositiveIntegerField(default=0)
    sex=models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
