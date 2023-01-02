from django.contrib import admin
from .models import Bill, Invoice

# Register your models here.


@admin.action(description="선택된 인보이스 발행을 시작합니다.")
def make_publish(self, request, queryset):
    queryset.update(issue=True)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "청구일",
            {
                "fields": (
                    "start_date",
                    "bill_date",
                )
            },
        ),
        (
            "공용전기료",
            {
                "fields": (
                    "total",
                    "maintanance",
                )
            },
        ),
        (
            "층별전기료",
            {
                "fields": (
                    "floor",
                    "basic",
                    "usage",
                )
            },
        ),
        (
            "전력 정보",
            {
                "fields": (
                    "usage_sum",
                    "ratio",
                    "unit_price",
                )
            },
        ),
        (
            "데이터 정보",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = (
        "__str__",
        "total",
        "public_share",
        "public_usage",
        "total_public",
        "floor",
        "none_tax",
        "usage_sum",
        "ratio",
        "unit_price",
        "area_cnt",
    )

    readonly_fields = (
        "start_date",
        "usage_sum",
        "ratio",
        "unit_price",
        "area_cnt",
        "area_sum",
        "created_at",
        "updated_at",
    )

    def usage_sum(self, obj):
        return obj.usage_sum()

    def ratio(self, obj):
        return obj.ratio()

    def unit_price(self, obj):
        return obj.unit_price()

    usage_sum.short_description = "검침량 총합"
    ratio.short_description = "소실율"
    unit_price.short_description = "단위당 단가"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "사용자 정보",
            {
                "fields": (
                    "contract",
                    "bill",
                    "usage",
                )
            },
        ),
        (
            "상세내역",
            {
                "fields": (
                    "basic",
                    "add_unit",
                    "without_tax",
                    "subtract_tax",
                    "add_tax",
                    "public",
                    "area_fee",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "청구요금",
            {
                "fields": ("total",),
            },
        ),
        (
            "데이터 정보",
            {
                "fields": (
                    "is_issue",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = (
        "contract",
        "is_issue",
        "bill",
        "usage",
        "without_tax",
        "subtract_tax",
        "add_tax",
        "public",
        "area_fee",
        "total",
    )

    readonly_fields = (
        "bill",
        "contract",
        "basic",
        "usage_ratio",
        "public",
        "area_fee",
        "without_tax",
        "subtract_tax",
        "add_tax",
        "without_tax",
        "add_unit",
        "add_tax",
        "total",
        "created_at",
        "updated_at",
    )
    actions = (make_publish,)
    list_filter = (
        "bill__bill_date",
        "is_issue",
    )
    ordering = (
        "bill",
        "contract",
    )

    def public(self, obj):
        return obj.public()

    def basic(self, obj):
        return int(obj.bill.basic * obj.contract.area / (obj.bill.area_sum))

    def add_unit(self, obj):
        if obj.bill.unit_price() and obj.usage:
            return int(obj.bill.unit_price() * obj.usage)

    def add_tax(self, obj):
        return obj.add_tax()

    def area_fee(self, obj):
        return obj.area_fee()

    def without_tax(self, obj):
        return obj.without_tax()

    def total(self, obj):
        return f"{obj.total()} 원"

    def subtract_tax(self, obj):
        return obj.add_tax() - obj.without_tax()

    basic.short_description = "전기 기본요금"
    add_unit.short_description = "전기사용량 요금"
    public.short_description = "2. 공용전기료 합계"
    area_fee.short_description = "3. 기본관리비"
    without_tax.short_description = "전기료 - 세전 전기료"
    subtract_tax.short_description = "부가세"
    add_tax.short_description = "1. 전기료 - 세후 합계"
    total.short_description = "1+2+3 합계"
