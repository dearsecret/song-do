from .models import Memo, Notice
from rest_framework import serializers


class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = (
            "pk",
            "title",
        )


class NoticeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        exclude = (
            "created_at",
            "updated_at",
        )


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        exclude = (
            "created_at",
            "updated_at",
        )
