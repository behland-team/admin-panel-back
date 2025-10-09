import rest_framework.serializers as serializers
from .models import FAQ, FAQCategory

class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = '__all__'