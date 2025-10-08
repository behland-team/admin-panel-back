from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeamMemberViewSet


router=DefaultRouter()
router.register(r'teams',TeamMemberViewSet,basename='teams')
urlpatterns =router.urls