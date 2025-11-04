# blog/views.py
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Category, Tag
from .serializer import PostSerializer, CategorySerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    - lookup با 'slug'
    - ادمین‌ها همه پست‌ها را می‌بینند
    - کاربران عادی فقط پست‌های Published و زمان‌رسیده (یا بدون زمان) را می‌بینند
    - favorites یک Boolean ساده است (با PATCH/PUT تغییر می‌کند)
    """
    serializer_class = PostSerializer
    lookup_field = "slug"

    # Search / filter / ordering
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

    def get_queryset(self):
        qs = (
            Post.objects.all()
            .select_related("author", "category")
            .prefetch_related("tags")
        )
        user = self.request.user
        if getattr(user, "is_staff", False):
            return qs
        now = timezone.now()
        return qs.filter(status=Post.Status.PUBLISHED).filter(
            Q(publish_at__isnull=True) | Q(publish_at__lte=now)
        )

    def perform_create(self, serializer):
        # اگر ساخت توسط کاربر ناشناس مجاز نیست، این خط FK را به کاربر فعلی ست می‌کند
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD برای دسته‌بندی‌ها؛ slug به‌صورت خودکار از name ساخته می‌شود.
    """
    queryset = Category.objects.all().order_by("-created_at")
    serializer_class = CategorySerializer
    lookup_field = "slug"

    # filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["created_at", "name"]
    filterset_fields = {"name": ["icontains"], "slug": ["exact"]}


class TagViewSet(viewsets.ModelViewSet):
    """
    CRUD برای تگ‌ها؛ slug به‌صورت خودکار از name ساخته می‌شود.
    """
    queryset = Tag.objects.all().order_by("-created_at")
    serializer_class = TagSerializer
    lookup_field = "slug"

    # filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["created_at", "name"]
    filterset_fields = {"name": ["icontains"], "slug": ["exact"]}
1