from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for the Task model."""
    list_display = ("id", "title", "owner", "priority", "status", "due_date", "created_at")
    list_filter = ("status", "priority", "due_date", "created_at")
    search_fields = ("title", "description", "owner__username", "owner__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "description", "owner")}),
        ("Task Details", {"fields": ("priority", "status", "due_date")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
