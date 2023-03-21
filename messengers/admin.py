from django.contrib import admin
from .models import SMS, SendLMS


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "to",
        "created_at",
    )
    readonly_fields = (
        "content",
        "invoice",
    )

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj=obj)


@admin.register(SendLMS)
class LMSAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "phone_number",
        "created_at",
        "sended",
    )

    readonly_fields = (
        "created_at",
        "sended",
    )

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj=obj)
