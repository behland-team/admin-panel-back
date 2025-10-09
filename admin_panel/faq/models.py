from django.db import models



class FAQCategory(models.Model):
    name = models.CharField(max_length=100, unique=True) 

    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE, 
        related_name="faqs" 
    )
    
    question = models.CharField(max_length=255)
    answer = models.TextField()

    class Meta:

        ordering = ['category', 'question'] 

    def __str__(self):

        return f"[{self.category.name}] {self.question}"