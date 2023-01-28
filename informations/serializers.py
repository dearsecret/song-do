from rest_framework.serializers import ModelSerializer
from .models import Customer, Billing


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
