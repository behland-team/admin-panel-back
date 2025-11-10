from django.db.models import Count, Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FAQCategory, FAQ
from .serializers import (
    FAQCategorySerializer,
    FAQSerializer,
    FAQCategoryDetailSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FAQCategoryViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r"\d+"
    queryset = FAQCategory.objects.all().annotate(faq_count=Count("faqs"))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "faq_count"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "retrieve" and self.request.query_params.get("include") == "faqs":
            return FAQCategoryDetailSerializer
        return FAQCategorySerializer

    @action(detail=True, methods=["get"])
    def faqs(self, request, pk=None):
        category = self.get_object()
        qs = category.faqs.all().order_by("question")
        search = request.query_params.get("search")
        if search:
            qs = qs.filter(Q(question__icontains=search) | Q(answer__icontains=search))
        page = self.paginate_queryset(qs)
        ser = FAQSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)
    
    @action(detail=False,methods=["get"], url_path="(?P<name>[^/.]+)")
    def by_name(self, request, name=None):
        try:
            category = FAQCategory.objects.get(name=name)
            faqs=category.faqs.all().order_by("question")
            serializer = FAQSerializer(faqs, many=True)
            return Response(serializer.data)

        except FAQCategory.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
       


class FAQViewSet(viewsets.ModelViewSet):
 
    queryset = FAQ.objects.select_related("category").all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category"]                 # ?category=<id>
    search_fields = ["question", "answer", "category__name"]
    ordering_fields = ["question", "category__name"]
    ordering = ["category__name", "question"]
