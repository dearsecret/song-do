from django.contrib import admin
from .models import Promotion

# Register your models here.


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "created_at",
    )
