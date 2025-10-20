# blog/serializers.py
from rest_framework import serializers
from .models import Post, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # نمایش نام نویسنده
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "summary", "content",
            "author", "category", "tags",
            "status", "publish_at", "is_featured", "image",
            "favorites", "created_at", "updated_at"
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]
