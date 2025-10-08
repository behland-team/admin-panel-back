from django.db import models

# Create your models here.

class RoadmapSection(models.Model):
    title=models.CharField(max_length=200)
    order=models.PositiveIntegerField()
    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title



class RoadmapItem(models.Model):
    section=models.ForeignKey(RoadmapSection,on_delete=models.CASCADE,related_name="items")
    description=models.TextField()
    order=models.IntegerField()
    is_completed=models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.description[:50]