from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DexEntryViewSet


router=DefaultRouter()
router.register(r'dex',DexEntryViewSet,basename='dex')
urlpatterns =router.urls