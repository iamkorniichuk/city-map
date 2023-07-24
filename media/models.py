from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ExpressionWrapper, Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

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
    attachment_type = models.CharField(_("attachment type"), max_length=64, blank=True)

    valid_content_types = []  # TODO: To end & Set GenericRelation in related models
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        limit_choices_to=valid_content_types,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        self.file_type = self.attachment.file.content_type
        self.check_content_type()
        super().save(*args, **kwargs)

    def check_content_type(self):
        if not type(self.content_object) in self.valid_content_types:
            raise ValidationError(
                f"Content object type need to be one of {self.valid_content_types}"
            )

    def delete(self, *args, **kwargs):
        self.attachment.close()
        self.attachment.delete(save=False)
        return super().delete(*args, **kwargs)
