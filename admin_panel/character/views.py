from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import character
from .serializers import CharacterSerializer

class CharacterViewSet(ModelViewSet):
    queryset = character.objects.all()
    serializer_class = CharacterSerializer