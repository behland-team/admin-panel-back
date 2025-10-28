from rest_framework import serializers
from .models import character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = character
        fields = '__all__'