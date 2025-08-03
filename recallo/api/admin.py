from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import StudyItem

User = get_user_model()


class StudyItemInline(admin.TabularInline):
    model = StudyItem
    extra = 0
    fields = ["title", "description", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "is_staff", "is_active"]
    search_fields = ["username", "email"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    ordering = [
        "username",
    ]

    inlines = [StudyItemInline]


@admin.register(StudyItem)
class StudyItemAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "title",
        "description",
        "user__email",
        "user__username",
    ]
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("user", "title", "description")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
