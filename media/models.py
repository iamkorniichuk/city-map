from django.db import models
from django.db.models import ExpressionWrapper, Q
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


# TODO: Delete unassigned files
class Media(models.Model):
    # TODO: Rename to attachment?
    file = models.FileField(
        _("file"),
        validators=[
            MimeTypeValidator(["image/*", "video/*"]),
        ],
    )
    content_type = models.CharField(_("type"), max_length=64, blank=True)

    def save(self, *args, **kwargs):
        self.content_type = self.file.file.content_type
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.close()
        self.file.delete(save=False)
        return super().delete(*args, **kwargs)
