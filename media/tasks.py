from apscheduler.schedulers.background import BackgroundScheduler

from .models import Media


def get_related_objects(model_class):
    return [
        f for f in model_class._meta.get_fields() if f.auto_created and not f.concrete
    ]


def delete_unassigned_files():
    fields = get_related_objects(Media)
    for field in fields:
        related_name = field.related_name
        filters = {related_name + "__isnull": True}
        number, objects = Media.objects.filter(**filters).delete()
        print(f"{number} unassigned files were deleted.")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_unassigned_files, "interval", weeks=1)
    scheduler.start()
