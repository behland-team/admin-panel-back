# blog/models.py
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    publish_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_featured = models.BooleanField(default=False)

    image = models.ImageField(upload_to="assets/blog/", blank=True, null=True)

    favorites = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    class Meta:
        ordering = ["-publish_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "publish_at"]),
        ]

    def __str__(self):
        return self.title



# class PostRating(TimeStampedModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     value = models.PositiveSmallIntegerField()  # 1..5

#     class Meta:
#         unique_together = ("post", "user")
