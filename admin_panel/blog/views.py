# blog/views.py
from django.db import models
from django.utils import timezone
from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend

from .models import Post
from .serializer import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    - lookup با slug
    - کاربران عادی فقط پست‌های منتشرشده و رسیده به زمان انتشار را می‌بینند
    - ادمین‌ها همه پست‌ها را می‌بینند
    - هیچ permission اختصاصی در این فایل تعریف نشده
    """
    serializer_class = PostSerializer
    lookup_field = "slug"

    # جست‌وجو/فیلتر/مرتب‌سازی
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "content", "slug", "category__name", "tags__name", "author__username"]
    ordering_fields = ["publish_at", "created_at", "title"]
    filterset_fields = {
        "status": ["exact"],
        "category__slug": ["exact"],
        "tags__slug": ["exact"],
        "is_featured": ["exact"],
        "favorites": ["exact"],
    }

    def get_base_queryset(self):
        return (
            Post.objects.all()
            .select_related("author", "category")
            .prefetch_related("tags")
        )

    def get_queryset(self):
        qs = self.get_base_queryset()
        user = self.request.user
        if getattr(user, "is_staff", False):
            return qs

        now = timezone.now()
        # فقط پست‌های منتشرشده‌ای که زمان‌شان رسیده (یا زمان ندارند)
        return qs.filter(status=Post.Status.PUBLISHED).filter(
            models.Q(publish_at__isnull=True) | models.Q(publish_at__lte=now)
        )

    def perform_create(self, serializer):
        # اگر Anonymous اجازه ساخت دارد، مدل Post باید author را nullable کند؛
        # در غیر این صورت اینجا همان کاربر فعلی را ست می‌کنیم.
        serializer.save(author=self.request.user)
