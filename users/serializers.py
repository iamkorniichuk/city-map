from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import User


# TODO: Doesn't use model fields
class UserTokenSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "Unable to log in with the provided credentials"
        )


# TODO: Separate changing password
class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }
