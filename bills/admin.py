from django.contrib import admin
from .models import Bill, Invoice, OwnerCharge

# from django.core.mail import send_mail
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings

# Register your models here.


@admin.action(description="선택된 항목의 입금을 확인으로 변경합니다.")
def make_publish(self, request, queryset):
    queryset.update(is_payed=True)


@admin.action(description="이메일을 발송합니다.")
def send_bill(self, request, queryset):
    for invoice in queryset:
        subject = (
            f"<송도비취타운> {invoice.contract.name} 전기료 및 관리비 {invoice.bill.__str__()} "
        )
        template = "customers/invoice.html"
        context = {
            "name": invoice.contract.name,
            "area": invoice.contract.area,
            "start": invoice.bill.start_date,
            "end": invoice.bill.bill_date,
            "usage": invoice.usage,
            "ratio_usage": invoice.ratio_usage,
            "public": invoice.public,
            "public_share": invoice.public_share,
            "area_fee": invoice.area_fee,
            "public_usage": invoice.public_usage,
            "basic": invoice.basic,
            "area_fee": invoice.area_fee,
            "tax": invoice.tax,
            "add_unit": invoice.add_unit,
            "total": invoice.total,
            "without_tax": invoice.without_tax,
            "add_tax": invoice.add_tax,
        }
        html_msg = render_to_string(template_name=template, context=context)
        plain_txt = strip_tags(html_msg)
        send_mail(
            subject,
            plain_txt,
            settings.EMAIL_HOST_USER,
            [invoice.contract.customer.username],
            html_message=html_msg,
        )


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
                    "get_usage_sum",
                    "unit_price",
                    "total_public",
                )
            },
        ),
        (
            "기타",
            {"fields": ("owner_charge",)},
        ),
        (
            "발행여부",
            {
                "fields": (
                    "is_ready",
                    "need_update",
                    "is_issue",
                ),
            },
        ),
        (
            "발행 정보",
            {
                "fields": (
                    "usage_sum",
                    "ratio",
                ),
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
        "is_issue",
        "total_public",
        "floor",
        "unit_price",
        "area_sum",
    )

    readonly_fields = (
        "start_date",
        "usage_sum",
        "get_usage_sum",
        "ratio",
        "unit_price",
        "area_sum",
        "is_ready",
        "need_update",
        "total_public",
        "created_at",
        "updated_at",
    )

    def get_usage_sum(self, obj):
        return obj.get_usage_sum()

    def ratio(self, obj):
        return obj.ratio()

    def is_ready(self, obj):
        return obj.is_ready()

    def need_update(self, obj):
        if obj.usage_sum != obj.get_usage_sum():
            return False
        else:
            return True

    is_ready.short_description = "발행 준비"
    need_update.short_description = "검산"
    get_usage_sum.short_description = "검침량 총합"
    ratio.short_description = "소실율"


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
                    "ratio_usage",
                )
            },
        ),
        (
            "상세내역",
            {
                "fields": (
                    "basic",
                    "add_unit",
                    "public",
                    "area_fee",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "청구요금",
            {
                "fields": (
                    "total",
                    "is_payed",
                ),
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
        "contract",
        "usage",
        "bill",
        "without_tax",
        "tax",
        "add_tax",
        "public",
        "area_fee",
        "total",
        "is_payed",
    )

    readonly_fields = (
        "bill",
        "contract",
        "basic",
        "public",
        "area_fee",
        "total",
        "ratio_usage",
        "add_unit",
        "without_tax",
        "tax",
        "add_tax",
        "created_at",
        "updated_at",
    )
    actions = (
        make_publish,
        send_bill,
    )
    list_filter = (
        "bill__bill_date",
        "is_payed",
        "bill",
    )
    ordering = (
        "-bill",
        "contract",
    )


@admin.register(OwnerCharge)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "charge",
    )
