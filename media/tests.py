from functools import wraps
from os.path import join
import magic

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Media


def open_media_files(names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            files = []
            for name in names:
                path = join(settings.MEDIA_ROOT, name)
                file = open(path, "rb").read()
                mime_type = magic.from_buffer(file, mime=True)
                files.append(SimpleUploadedFile(name, file, content_type=mime_type))

            result = func(*args, **kwargs, files=files)

            for file in files:
                file.close()

            return result

        return wrapper

    return decorator


class MediaListTestCase(TestCase):  # TODO: Delete downloaded files after testing
    client = Client()
    url = reverse("media:list")

    @open_media_files(["image.jpg", "transparent_image.png", "video.mp4"])
    def test_multiple_files_upload(self, files):
        response = self.client.post(self.url, {"media": files})

        json = response.json()
        equal_length = len(files) == len(json)
        models_exists = all([Media.objects.filter(pk=data["id"]) for data in json])
        assert equal_length and models_exists
