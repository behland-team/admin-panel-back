import rest_framework.serializers as serializers
from .models import RoadmapItem, RoadmapSection

class RoadmapItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapItem
        fields = '__all__'


class RoadmapSectionSerializer(serializers.ModelSerializer):
    items = RoadmapItemSerializer(many=True, read_only=True)

    class Meta:
        model = RoadmapSection
        fields = '__all__'