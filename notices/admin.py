from django.contrib import admin
from .models import Notice, Memo

# Register your models here.


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    readonly_fields = ("writer",)
    list_display = (
        "title",
        "writer",
        "created_at",
    )


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = (
        "comment",
        "created_at",
        "bill",
    )
