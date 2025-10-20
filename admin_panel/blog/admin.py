# blog/admin.py
from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")   # مهم برای autocomplete

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")   # مهم برای autocomplete

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "publish_at", "is_featured")
    list_filter  = ("status", "category", "tags")
    search_fields = ("title", "content", "slug")  # (برای خود Post)
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")  # این به search_fields ادمین‌های بالا نیاز دارد
