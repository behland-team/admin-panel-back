from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer