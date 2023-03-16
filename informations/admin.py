from django.contrib import admin
from .models import Customer, Billing, Accounting


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "custNum",
        "title",
    )


@admin.register(Billing)
class BillDataAdmin(admin.ModelAdmin):
    pass


@admin.register(Accounting)
class AccountingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kind",
        "price",
        "date",
    )
