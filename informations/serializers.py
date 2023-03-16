from rest_framework.serializers import ModelSerializer
from .models import Customer, Billing, Accounting
from realtimes.models import WeatherFcst


class CustSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "title",
            "custNum",
        )


class BillingSerializer(ModelSerializer):
    custNo = CustSerializer(read_only=True)

    class Meta:
        model = Billing
        exclude = (
            "created_at",
            "updated_at",
        )


class WeatherSerializer(ModelSerializer):
    class Meta:
        model = WeatherFcst
        exclude = (
            "created_at",
            "updated_at",
        )


class AccountingSerializer(ModelSerializer):
    class Meta:
        model = Accounting
        exclude = (
            "created_at",
            "updated_at",
        )
