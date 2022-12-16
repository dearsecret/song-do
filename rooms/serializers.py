from rest_framework import serializers
from .models import Kind, Facility, Room
from users.serializers import PrivateUserSerializer


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = "__all__"


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)
    kind = KindSerializer(read_only=True)
    host = PrivateUserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
