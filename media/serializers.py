from rest_framework import serializers

from .models import Media


class NestedMediaSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = Media.objects.get(**validated_data)
        return instance

    class Meta:
        model = Media
        fields = ("attachment", "attachment_type")
        extra_kwargs = {
            "attachment": {"read_only": True},
            "attachment_type": {"read_only": True},
        }


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ("content_type", "object_id")
        extra_kwargs = {
            "attachment_type": {"read_only": True},
        }
