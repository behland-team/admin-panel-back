# blog/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
# from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("author", "category").prefetch_related("tags")
    # serializer_class = PostSerializer
    lookup_field = "slug"  # به‌جای id از slug استفاده می‌کنیم

    # فقط پست‌های منتشرشده را به همه نشون بده
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # ادمین می‌تونه همه رو ببینه
            return Post.objects.all()
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def perform_create(self, serializer):
        # موقع ساخت پست جدید نویسنده را خودکار ست کن
        serializer.save(author=self.request.user)

    # endpoint برای لیست علاقه‌مندی‌ها
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, slug=None):
        post = self.get_object()
        user = request.user
        if user in post.favorites.all():
            post.favorites.remove(user)
            return Response({"status": "removed from favorites"})
        post.favorites.add(user)
        return Response({"status": "added to favorites"})
