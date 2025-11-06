# blog/views.py
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Category, Tag
from .serializer import PostSerializer, CategorySerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]  # همه GET، فقط لاگین برای تغییرات

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
            # ادمین همه چی رو می‌بینه
            return qs
        # بقیه فقط منتشرشده‌هایی که زمان انتشارشون رسیده
        now = timezone.now()
        return qs.filter(
            status=Post.Status.PUBLISHED
        ).filter(
            Q(publish_at__isnull=True) | Q(publish_at__lte=now)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(detail=False, methods=["get"], url_path="by-category/(?P<category_name>[^/.]+)")
    def by_category_name(self, request, category_name=None):
        try:
            category = Category.objects.get(name=category_name)
            posts = Post.objects.filter(category=category).order_by("title")
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {"error": f"Category '{category_name}' not found"}, 
                status=404
            )
        
    @action(detail=False,methods=["get"],url_path="limit/(?P<post_limit>[^/.]+)")
    def limited(self , request,post_limit=None):
        try:
            limit=int(request.query_params.get("limit", post_limit))   
            if limit<0:
                return Response({"error":"Limit must be a non-negative integer."},status=400)
            posts=Post.objects.all().order_by("-publish_at")[:limit]
            serializer=PostSerializer(posts,many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error":"Limit must be an integer."},status=400)   

    @action(detail=False ,methods=["get"])
    def favorites(self,request):
       favorite_post=Post.objects.filter(favorites=True).order_by("-publish_at")
       serializer=PostSerializer(favorite_post,many=True)
       return Response(serializer.data)
    


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