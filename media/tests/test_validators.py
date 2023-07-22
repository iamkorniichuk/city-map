from django.test import TestCase

from media.validators import MimeTypeValidator


class MimeTypeValidatorTestCase(TestCase):
    patterns = ["image/png", "*/webm", "text/*"]
    validator = MimeTypeValidator(patterns)

    def test_pattern_converting(self):
        full_match = self.validator.is_type_valid("image/png")
        leading_asterisk = self.validator.is_type_valid("video/webm")
        final_asterisk = self.validator.is_type_valid("text/plain")
        invalid = self.validator.is_type_valid("videoimage/png") == False
        assert full_match and leading_asterisk and final_asterisk and invalid

    # TODO: To end
    def test_mime_recognition(self):
        ...
