from rest_framework import serializers
from .models import FAQCategory, FAQ


class FAQCategorySerializer(serializers.ModelSerializer):
    faq_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FAQCategory
        fields = ["id", "name", "faq_count"]


class FAQSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = FAQ
        fields = ["id", "category", "category_name", "question", "answer"]

    def validate(self, attrs):
        # جلوگیری از تکرار سوال داخل یک کتگوری (اختیاری و نرم)
        category = attrs.get("category") or getattr(self.instance, "category", None)
        question = attrs.get("question") or getattr(self.instance, "question", None)
        if category and question:
            qs = FAQ.objects.filter(category=category, question__iexact=question)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("این سؤال در این دسته‌بندی قبلاً ثبت شده است.")
        return attrs


class FAQCategoryDetailSerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = FAQCategory
        fields = ["id", "name", "faqs"]
