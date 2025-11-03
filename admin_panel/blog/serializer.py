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
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # فیلدهای ورودی برای نوشتن
    category_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    tag_slugs = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "summary", "content",
            "author", "category", "tags",
            "status", "publish_at", "is_featured", "image",
            "favorites",
            "created_at", "updated_at",
            # write helpers
            "category_slug", "tag_slugs",
        ]
        read_only_fields = ["slug", "created_at", "updated_at", "author"]

    def create(self, validated_data):
        category_obj = validated_data.pop("category_slug", None)
        tag_objs = validated_data.pop("tag_slugs", [])
        post = super().create(validated_data)
        if category_obj is not None:
            post.category = category_obj
            post.save(update_fields=["category"])
        if tag_objs:
            post.tags.set(tag_objs)
        return post

    def update(self, instance, validated_data):
        category_obj = validated_data.pop("category_slug", None)
        tag_objs = validated_data.pop("tag_slugs", None)
        post = super().update(instance, validated_data)
        if category_obj is not None:
            post.category = category_obj
            post.save(update_fields=["category"])
        if tag_objs is not None:
            post.tags.set(tag_objs)
        return post
