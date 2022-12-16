from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Basic Info", {"fields": ("username", "name", "avatar")}),
        ("Personal info", {"fields": ("phone", "email", "gender")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_host",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = (
        "username",
        "last_login",
    )
