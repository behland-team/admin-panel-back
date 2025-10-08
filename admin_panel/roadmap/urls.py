from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoadmapSectionViewSet, RoadmapItemViewSet

router = DefaultRouter()
router.register(r'sections', RoadmapSectionViewSet)
router.register(r'items', RoadmapItemViewSet)
urlpatterns =router.urls