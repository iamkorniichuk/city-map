from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

import magic
import re


@deconstructible
class MimeTypeValidator:
    def __init__(self, type_patterns):
        self.type_patterns = type_patterns

    def __call__(self, value):
        file = value.file.read()
        mime_type = magic.from_buffer(file, mime=True)

        if not self.is_type_valid(mime_type):
            raise ValidationError(
                _(
                    f"{value.name} has invalid MIME type ({mime_type}). Use these types: {', '.join(self.type_patterns)}"
                )
            )

    def is_type_valid(self, mime_type):
        for pattern in self.type_patterns:
            regex = self.convert_pattern_to_regex(pattern)
            if re.match(regex, mime_type):
                return True
        return False

    @classmethod
    def convert_pattern_to_regex(cls, pattern):
        return "^" + pattern.replace("*", ".+") + "$"

    def __eq__(self, other):
        return self.type_patterns == other.types
