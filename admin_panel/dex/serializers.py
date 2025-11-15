from .models import DexEntry
from rest_framework import serializers


class DexEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DexEntry
        fields = '__all__'