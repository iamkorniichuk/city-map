from django.test import TestCase

from media.validators import MimeTypeValidator


class MimeTypeValidatorTestCase(TestCase):
    patterns = ["image/png", "*/webm", "text/*"]
    validator = MimeTypeValidator(patterns)

    def test_full_match(self):
        assert self.validator.is_type_valid("image/png")

    def test_leading_asterisk(self):
        assert self.validator.is_type_valid("video/webm")

    def test_final_asterisk(self):
        assert self.validator.is_type_valid("text/plain")

    def test_invalid(self):
        assert self.validator.is_type_valid("videoimage/png") == False
