from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet


router=DefaultRouter()
router.register(r'chcaracters',CharacterViewSet,basename='chcaracters')
urlpatterns =router.urls