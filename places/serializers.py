from rest_framework import serializers

from media.serializers import MediaSerializer

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)

    class Meta:
        model = Place
        fields = "__all__"
        extra_kwargs = {
            "slug": {"read_only": True},
        }
