from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from media.serializers import NestedMediaSerializer

from .models import Place


class PlaceSerializer(WritableNestedModelSerializer):
    media = NestedMediaSerializer(many=True, allow_empty=False)
    url = serializers.URLField(source="get_absolute_url", read_only=True)

    class Meta:
        model = Place
        fields = "__all__"
        extra_kwargs = {
            "slug": {"read_only": True},
        }
