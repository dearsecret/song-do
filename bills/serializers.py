from rest_framework import serializers
from .models import Invoice, Bill


class BillListSerializer(serializers.ModelSerializer):

    start_date = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = (
            "pk",
            "__str__",
            "start_date",
            "bill_date",
        )

    def get_start_date(self, bill):
        return bill.start_date()


class BillDetailSerializer(serializers.ModelSerializer):

    usage_sum = serializers.SerializerMethodField()
    public_share = serializers.SerializerMethodField()
    public_usage = serializers.SerializerMethodField()
    total_public = serializers.SerializerMethodField()
    none_tax = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    ratio = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        exclude = (
            "created_at",
            "updated_at",
        )

    def get_usage_sum(self, bill):
        return bill.usage_sum()

    def get_public_share(self, bill):
        return bill.public_share()

    def get_public_usage(self, bill):
        return bill.public_usage()

    def get_total_public(self, bill):
        return bill.total_public()

    def get_none_tax(self, bill):
        return bill.none_tax()

    def get_unit_price(self, bill):
        return bill.unit_price()

    def get_ratio(self, bill):
        return bill.ratio()


class InvoiceListSerializer(serializers.ModelSerializer):
    bill = BillListSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "pk",
            "bill",
            "__str__",
            "usage",
        )


class InvoiceDetailSerializer(serializers.ModelSerializer):
    bill = BillListSerializer(read_only=True)

    without_tax = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    add_tax = serializers.SerializerMethodField()
    public_share = serializers.SerializerMethodField()
    public_usage = serializers.SerializerMethodField()
    public = serializers.SerializerMethodField()
    area_fee = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = (
            "pk",
            "is_issue",
            "bill",
            "__str__",
            "usage",
            "bill",
            "without_tax",
            "tax",
            "add_tax",
            "public_share",
            "public_usage",
            "public",
            "area_fee",
            "total",
        )

    def without_tax(self, invoice):
        return invoice.get_without_tax()

    def tax(self, invoice):
        return invoice.get_tax()

    def add_tax(self, invoice):
        return invoice.get_add_tax()

    def public_share(self, invoice):
        return invoice.get_public_share()

    def public_usage(self, invoice):
        return invoice.get_public_usage()

    def public(self, invoice):
        return invoice.get_public()

    def area_fee(self, invoice):
        return invoice.get_area_fee()

    def total(self, invoice):
        return invoice.get_total()
