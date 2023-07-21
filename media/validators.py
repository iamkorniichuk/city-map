from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

import magic


@deconstructible
class MimeTypeValidator:
    def __init__(self, types):
        self.types = types

    def __call__(self, value):
        file = value.file.read()
        mime_type = magic.from_buffer(file, mime=True)
        for type in self.types:
            if type in mime_type:
                return True
        raise ValidationError(
            _(
                f"{value.name} has invalid MIME type ({mime_type}). Use these types: {', '.join(self.types)}"
            )
        )

    def __eq__(self, other):
        return self.types == other.types
