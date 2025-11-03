# blog/admin.py
from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "publish_at", "is_featured", "favorites")
    list_filter  = ("status", "category", "tags", "is_featured", "favorites")
    search_fields = ("title", "content", "slug")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")
