# blog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet  # ویویی که قبلاً ساختی

# router مسیرهای CRUD را خودش می‌سازد
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
