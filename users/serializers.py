from rest_framework.serializers import ModelSerializer
from .models import User


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "avatar",
        )
