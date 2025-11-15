from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import DexEntry
from .serializers import DexEntrySerializer

class DexEntryViewSet(ModelViewSet):
    queryset = DexEntry.objects.all()
    serializer_class = DexEntrySerializer   

    