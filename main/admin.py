from django.contrib import admin

from main.models import Experience, Project


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "started_at", "ended_at", "is_ongoing")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "project_url")
    list_filter = ("category",)
    search_fields = ("title", "category", "description")
    readonly_fields = ("id", "created_at")


