from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet, FAQCategoryViewSet


router = DefaultRouter()
router.register(r'faq', FAQViewSet)
router.register(r'category', FAQCategoryViewSet)
urlpatterns =router.urls