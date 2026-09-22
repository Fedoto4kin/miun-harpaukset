from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from lessons.models import LessonSpeech


class LessonSpeechCodeTests(SimpleTestCase):
    def test_valid_codes(self):
        for code in ("1.0", "1.1", "12.34", "0.0"):
            speech = LessonSpeech(code=code)
            speech.clean()

    def test_invalid_codes(self):
        for code in ("1", "1.", ".1", "1.2.3", "a.b", "1-2", " 1.0"):
            speech = LessonSpeech(code=code)
            with self.assertRaises(ValidationError, msg=code) as ctx:
                speech.clean()
            self.assertIn("code", ctx.exception.message_dict)

    def test_empty_code_allowed(self):
        for code in (None, ""):
            speech = LessonSpeech(code=code)
            speech.clean()
