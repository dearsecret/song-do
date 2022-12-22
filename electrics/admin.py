from django.contrib import admin
from .models import Electric

# Register your models here.


@admin.register(Electric)
class ElectricAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "req_amt",
    )
