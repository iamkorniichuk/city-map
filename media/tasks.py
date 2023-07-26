from apscheduler.schedulers.background import BackgroundScheduler

from .models import Media


def delete_unassigned_files():
    number, objects = Media.objects.filter(object_id__isnull=True).delete()
    print(f"{number} unassigned files were deleted.")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_unassigned_files, "interval", weeks=1)
    scheduler.start()
