from django.contrib import admin
from character.models import character

# Register your models here.
@admin.register(character)
class CharacterAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display=('name', 'created_at',)
    ordering=('created_at',)
# admin.site.register(character)
