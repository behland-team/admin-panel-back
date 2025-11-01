

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet, FAQCategoryViewSet

router = DefaultRouter()
router.register(r"faq-categories", FAQCategoryViewSet, basename="faqcategory")
router.register(r"faqs", FAQViewSet, basename="faq")

urlpatterns =router.urls
