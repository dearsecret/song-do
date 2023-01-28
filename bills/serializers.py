from rest_framework import serializers
from .models import Invoice, Bill, OwnerCharge
from contracts.serializers import ContractSerializer
from notices.serializers import MemoSerializer


class OwnerChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerCharge
        exclude = (
            "created_at",
            "updated_at",
        )


class BillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            "pk",
            "__str__",
            "start_date",
            "bill_date",
        )


class BillDetailSerializer(serializers.ModelSerializer):
    owner_charge = OwnerChargeSerializer(many=True, read_only=True)
    memos = MemoSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        exclude = (
            "created_at",
            "updated_at",
        )


class InvoiceListSerializer(serializers.ModelSerializer):
    bill = BillListSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "pk",
            "is_payed",
            "bill",
            "__str__",
            "usage",
        )


class InvoiceDetailSerializer(serializers.ModelSerializer):
    bill = BillDetailSerializer(read_only=True)
    contract = ContractSerializer(read_only=True)

    class Meta:
        model = Invoice
        exclude = (
            "created_at",
            "updated_at",
        )
