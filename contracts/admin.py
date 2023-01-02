from django.contrib import admin
from .models import Contract

# Register your models here.


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "rent",
    )
