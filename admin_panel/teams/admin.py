from django.contrib import admin
from teams.models import TeamMember
# Register your models here.

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "created_at","order")
    search_fields = ("full_name", "position")
    ordering = ("full_name","order")