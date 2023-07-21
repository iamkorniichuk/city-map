from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ContentTypeValidator:
    def __init__(self, types):
        self.types = types

    def __call__(self, value):
        for type in self.types:
            if type in value.content_type:
                return True
        raise ValidationError(
            _(
                f"{value.name} has invalid content type ({value.content_type}). Use below content types: {', '.join(self.types)}"
            )
        )

    def __eq__(self, other):
        return self.types == other.types
