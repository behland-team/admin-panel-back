from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)
    #Author = models.PositiveIntegerField()
    #category
    rate=models.PositiveIntegerField(default=0)
    # tags
    # image
    favorites = models.BooleanField(default=False)

