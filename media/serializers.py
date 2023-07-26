from rest_framework import serializers

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
        # exclude = ("content_type", "object_id", "content_object")
        extra_kwargs = {
            "attachment_type": {"read_only": True},
        }
