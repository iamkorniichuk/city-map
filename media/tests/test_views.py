from functools import wraps
from os.path import join
import magic

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from media.models import Media


def open_test_files(names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            files = []
            for name in names:
                path = join(settings.MEDIA_ROOT, "test", name)
                file = open(path, "rb").read()
                mime_type = magic.from_buffer(file, mime=True)
                files.append(SimpleUploadedFile(name, file, content_type=mime_type))

            result = func(*args, **kwargs, files=files)

            for file in files:
                file.close()

            return result

        return wrapper

    return decorator


class MediaListTestCase(TestCase):
    url = reverse("media:list")
    client = Client()

    def setUp(self):
        self.models = []

    @open_test_files(["image.jpg", "transparent_image.png", "video.mp4"])
    def test_multiple_files_upload(self, files):
        response = self.client.post(self.url, {"media": files})

        for id in [data["id"] for data in response.json()]:
            self.models.append(Media.objects.get(pk=id))

        assert len(files) == len(self.models)

    def tearDown(self):
        for model in self.models:
            model.delete()
