from django.test import TestCase

from .models import Base, Word


class WordTestClass(TestCase):

    def test_search_prepare(self):
        search = "ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖüÜ'’"
        self.assertEqual(Word.search_prepare(search), "abcčdefghijklmnoprsšzžtuvyäöyy")

    def test_krl_slugify(self):
        search = "ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖÜ'’"
        self.assertEqual(
            Base.krl_slugify(Base, search), "abcčdefghijklmnoprsšzžtuvyäöy"
        )
