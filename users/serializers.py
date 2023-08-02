from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import User


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "Unable to log in with the provided credentials"
        )


class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


# TODO: Add changing password
