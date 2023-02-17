from rest_framework.serializers import ModelSerializer
from .models import Promotion


class PromotionListSerializer(ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            "pk",
            "title",
            "thumb",
            "category",
        )


class PromotionDetialSerializer(ModelSerializer):
    class Meta:
        model = Promotion
        exclude = ("updated_at",)
