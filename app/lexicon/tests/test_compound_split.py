"""Слитные сложения: разрез по словарю + fallback поиска."""

from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from lexicon.compound_split import (
    find_best_compound_split,
    find_compound_splits,
    score_split,
)
from lexicon.models import GrammarForm, Pos, Word, WordForm


class CompoundSplitUnitTests(SimpleTestCase):
    def test_score_prefers_gen_left_and_head_right(self):
        heads = {"kieli", "paikka"}
        a = score_split("muamon", "kieli", head_rights=heads)
        b = score_split("muamo", "nkieli", head_rights=heads)
        self.assertGreater(a, b)

    def test_too_short(self):
        self.assertEqual(find_compound_splits("ab"), [])


class CompoundSplitDbTests(TestCase):
    def setUp(self):
        self.pos = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.gf_nom = GrammarForm.objects.create(
            code="nom_sg",
            name_krl="yksikön nominativa",
            name_ru="номинатив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=10,
        )
        self.gf_gen = GrammarForm.objects.create(
            code="gen_sg",
            name_krl="yksikön genetiva",
            name_ru="генитив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=20,
        )

        self.muamo = Word(word="muam|o", pos=self.pos)
        self.muamo.save()
        WordForm.objects.create(
            word=self.muamo, grammar_form=self.gf_nom, form="muamo"
        )
        WordForm.objects.create(
            word=self.muamo, grammar_form=self.gf_gen, form="muamon"
        )

        self.kieli = Word(word="kiel|i", pos=self.pos)
        self.kieli.save()
        WordForm.objects.create(
            word=self.kieli, grammar_form=self.gf_nom, form="kieli"
        )

        self.elanda = Word(word="elän|dä", pos=self.pos)
        self.elanda.save()
        WordForm.objects.create(
            word=self.elanda, grammar_form=self.gf_nom, form="eländä"
        )

        self.paikka = Word(word="paik|ka", pos=self.pos)
        self.paikka.save()
        WordForm.objects.create(
            word=self.paikka, grammar_form=self.gf_nom, form="paikka"
        )

        self.pitkakieli = Word(word="pitkäkiel|i", pos=self.pos)
        self.pitkakieli.save()
        WordForm.objects.create(
            word=self.pitkakieli, grammar_form=self.gf_nom, form="pitkäkieli"
        )

    def test_split_muamonkieli(self):
        best = find_best_compound_split("muamonkieli")
        self.assertIsNotNone(best)
        self.assertEqual(best.left, "muamon")
        self.assertEqual(best.right, "kieli")

    def test_split_elandapaikka(self):
        best = find_best_compound_split("eländäpaikka")
        self.assertIsNotNone(best)
        self.assertEqual(best.left, "eländä")
        self.assertEqual(best.right, "paikka")

    def test_search_api_compound_muamonkieli(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "muamonkieli"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        words = [r["word"] for r in rows]
        self.assertIn("muam|o", words)
        self.assertIn("kiel|i", words)
        self.assertTrue(all(r.get("compound_parts") == ["muamon", "kieli"] for r in rows))
        self.assertTrue(all(r.get("compound_of") == "muamonkieli" for r in rows))

    def test_search_api_compound_elandapaikka(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "eländäpaikka"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        words = {r["word"] for r in rows}
        self.assertIn("elän|dä", words)
        self.assertIn("paik|ka", words)
        self.assertEqual(rows[0]["compound_parts"], ["eländä", "paikka"])

    def test_search_api_whole_lemma_not_split(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "pitkäkieli"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["word"], "pitkäkiel|i")
        self.assertIsNone(rows[0].get("compound_parts"))

    def test_search_api_unknown_stays_empty(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "xxxxxxxx"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])
