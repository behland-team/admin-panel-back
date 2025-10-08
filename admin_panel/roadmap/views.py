from rest_framework.viewsets import ModelViewSet
from .models import RoadmapSection, RoadmapItem
from .serializers import RoadmapSectionSerializer, RoadmapItemSerializer

class RoadmapSectionViewSet(ModelViewSet):
    queryset = RoadmapSection.objects.all().order_by('order')
    serializer_class = RoadmapSectionSerializer


class RoadmapItemViewSet(ModelViewSet):
    queryset = (RoadmapItem.objects
                .select_related('section')
                .all()
                .order_by('section__order', 'order'))
    serializer_class = RoadmapItemSerializer

    filterset_fields = ['section', 'is_completed']
    search_fields = ['description']
    ordering_fields = ['order', 'section__order']
