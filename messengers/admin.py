from django.contrib import admin
from .models import SMS


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    pass
