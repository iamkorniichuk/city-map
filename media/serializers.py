from rest_framework import serializers

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ("content_type", "object_id")
        extra_kwargs = {
            "attachment_type": {"read_only": True},
        }
