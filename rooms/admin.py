from django.contrib import admin
from .models import Room, Kind, Facility


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "deposit",
        "price",
        "host",
    )
    list_filter = ("city",)

    search_fields = ("host.name",)


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
