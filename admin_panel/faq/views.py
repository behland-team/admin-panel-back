from django.shortcuts import render
from rest_framework import viewsets
from .models import FAQ, FAQCategory
from .serializers import FAQSerializer, FAQCategorySerializer


class FAQCategoryViewSet(viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all().order_by('name')
    serializer_class = FAQCategorySerializer
    search_fields = ['name']
    ordering_fields = ['name']


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.select_related('category').all().order_by('category__name', 'question')
    serializer_class = FAQSerializer

    filterset_fields = ['category']
    search_fields = ['question', 'answer']
    ordering_fields = ['category__name', 'question']

