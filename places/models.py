from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from media.models import Media


class CoordinateField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        decimal_places = kwargs.pop("decimal_places", 6)
        max_digits = kwargs.pop("max_digits", 9)
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, *args, **kwargs
        )


class Place(models.Model):
    name = models.CharField(_("name"), max_length=64)
    latitude = CoordinateField(_("latitude"))
    longitude = CoordinateField(_("longitude"))
    description = models.TextField(_("description"))
    media = GenericRelation(Media)

    def get_location(self):
        return {"x": self.latitude, "y": self.longitude}

    def set_location(self, point):
        self.latitude = point["x"]
        self.longitude = point["y"]

    location = property(get_location, set_location)

    def __str__(self):
        return self.name
