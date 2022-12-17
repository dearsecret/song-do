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
    kind = KindSerializer(read_only=True)
    host = PrivateUserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "city",
            "kind",
            "deposit",
            "host",
            "is_owner",
        )

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return request.user == room.owner
        return False


class RoomDetailSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)
    kind = KindSerializer(read_only=True)
    host = PrivateUserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return request.user == room.owner
        return False
