from django.contrib import admin
from .models import Contract, Rent

# Register your models here.


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "rent",
    )


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ("usage_end", "is_payed", "contract", "__str__")

    readonly_fields = (
        "payed_cnt",
        "usage_end",
        "contract",
        "is_payed",
    )

    ordering = (
        "check_date",
        "usage_end",
    )

    def is_payed(self, obj):
        return obj.get_is_payed()

    is_payed.short_description = "지불 여부"
