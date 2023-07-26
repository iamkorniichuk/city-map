from django.db import models
from django.db.models import ExpressionWrapper, Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

import magic

from .validators import MimeTypeValidator


class MediaManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_image=ExpressionWrapper(
                    Q(content_type__contains="image"),
                    output_field=models.BooleanField(),
                ),
                is_video=ExpressionWrapper(
                    Q(content_type__contains="video"),
                    output_field=models.BooleanField(),
                ),
            )
        )


class Media(models.Model):
    attachment = models.FileField(
        _("attachment"),
        validators=[
            MimeTypeValidator(["image/*", "video/*"]),
        ],
    )
    attachment_type = models.CharField(
        _("attachment type"), max_length=64, blank=True, editable=False
    )

    valid_content_types = []  # TODO: To end & Set GenericRelation in related models
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        limit_choices_to=valid_content_types,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_attachment_type()
        super().save(update_fields=["attachment_type"])

    def set_attachment_type(self):
        file = self.attachment.file
        self.attachment_type = magic.from_buffer(file.read(1024), mime=True)
        file.close()

    def delete(self, *args, **kwargs):
        self.attachment.close()
        self.attachment.delete(save=False)
        return super().delete(*args, **kwargs)
