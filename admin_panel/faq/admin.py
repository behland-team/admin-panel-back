from django.contrib import admin
from django.db.models import Count
from .models import FAQCategory, FAQ


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ("question", "answer")
    show_change_link = True


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "faq_count")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [FAQInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_faq_count=Count("faqs"))

    def faq_count(self, obj):
        return getattr(obj, "_faq_count", 0)
    faq_count.short_description = "FAQs"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category")
    list_filter = ("category",)
    search_fields = ("question", "answer", "category__name")
    ordering = ("category__name", "question")
