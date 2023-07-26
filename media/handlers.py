from django.db.models import signals
from django.dispatch import receiver

from .models import Media


@receiver(signals.post_delete, sender=Media)
def auto_delete_files(sender, instance, *args, **kwargs):
    instance.attachment.close()
    instance.attachment.delete(save=False)
