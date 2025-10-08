from django.contrib import admin
from .models import RoadmapSection, RoadmapItem

class RoadmapItemInline(admin.TabularInline):
    model = RoadmapItem
    extra = 1

@admin.register(RoadmapSection)
class RoadmapSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)
    inlines = [RoadmapItemInline]

@admin.register(RoadmapItem)
class RoadmapItemAdmin(admin.ModelAdmin):
    list_display = ("section", "description", "is_completed", "order")
    list_filter = ("section", "is_completed")
    search_fields = ("description",)
    ordering = ("section", "order")
