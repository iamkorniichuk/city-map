from django.apps import AppConfig


class MediaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "media"

    def ready(self):
        from . import tasks
        from .handlers import auto_delete_files

        tasks.start()
