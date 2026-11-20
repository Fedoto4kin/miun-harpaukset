"""Reverse-поиск по переводам: ё и е эквивалентны."""

from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from lexicon.models import Definition, Pos, Word
from lexicon.search import normalize_definition_search


class NormalizeDefinitionSearchTests(SimpleTestCase):
    def test_yo_to_ye(self):
        self.assertEqual(
            normalize_definition_search("Ягнёнок"),
            "ягненок",
        )
        self.assertEqual(
            normalize_definition_search("козлёнок"),
            "козленок",
        )

    def test_empty(self):
        self.assertEqual(normalize_definition_search(""), "")


class DefinitionLcaseSaveTests(TestCase):
    def setUp(self):
        self.pos = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.word = Word(word="vuonna", pos=self.pos)
        self.word.save()

    def test_save_normalizes_yo(self):
        d = Definition(
            word=self.word,
            lang="ru",
            definition="ягнёнок, козлёнок",
        )
        d.save()
        self.assertEqual(d.definition_lcase, "ягненок, козленок")
        self.assertEqual(d.definition, "ягнёнок, козлёнок")


class ReverseSearchApiTests(TestCase):
    def setUp(self):
        self.pos = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.word = Word(word="vuonna", pos=self.pos)
        self.word.save()
        Definition.objects.create(
            word=self.word,
            lang="ru",
            definition="ягненок",
        )
        self.client = APIClient()

    def test_reverse_search_with_yo(self):
        resp = self.client.get(
            "/api/v0/lexicon/reverse/", {"query": "ягнёнок"}
        )
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertIn("vuonna", words)

    def test_reverse_search_with_ye(self):
        resp = self.client.get(
            "/api/v0/lexicon/reverse/", {"query": "ягненок"}
        )
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertIn("vuonna", words)

    def test_reverse_suggestions_with_yo(self):
        resp = self.client.get(
            "/api/v0/lexicon/reverse-search-suggestions/",
            {"query": "ягнё"},
        )
        self.assertEqual(resp.status_code, 200)
        defs = {row["word"] for row in resp.json()}
        self.assertIn("ягненок", defs)
