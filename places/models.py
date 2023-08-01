from django.db import models
from django.db.models import ExpressionWrapper, Q
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from common.utils import unique_slugify
from media.models import Media
from users.models import User


class CoordinateField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        decimal_places = kwargs.pop("decimal_places", 6)
        max_digits = kwargs.pop("max_digits", 9)
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, *args, **kwargs
        )


class PlaceManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                has_owner=ExpressionWrapper(
                    Q(owner__isnull=False),
                    output_field=models.BooleanField(),
                )
            )
        )


class Place(models.Model):
    name = models.CharField(_("name"), max_length=64)
    slug = models.SlugField(_("slug"), unique=True, blank=True, editable=False)
    latitude = CoordinateField(_("latitude"))
    longitude = CoordinateField(_("longitude"))
    description = models.TextField(_("description"))
    media = GenericRelation(Media)

    owner = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="places",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.name, Place)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("places:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
