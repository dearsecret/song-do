from rest_framework import serializers
from .models import Kind, Facility


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = "__all__"


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"
