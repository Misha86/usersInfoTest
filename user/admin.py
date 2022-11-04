"""Configuration for admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    """Class for specifying CustomUser fields in admin."""

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("username", "first_name", "last_name", "is_superuser", "is_active", "id")
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar", "date_joined")}),
        ("Permissions", {"fields": ("is_active", )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name",
                       "avatar", "password1", "password2"),
        }),
    )
    search_fields = ("username",)
    ordering = ("id",)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
