"""Притяжательные -ni / -š: поиск-цепочка, не в парадигме."""

from django.test import TestCase
from rest_framework.test import APIClient

from lexicon.models import GrammarForm, Pos, Stem, Word, WordForm
from lexicon.wordform_gen.possessives import (
    build_dim_ze_stem,
    generate_possessive_forms,
    pick_vowel_stem,
)
from lexicon.management.commands.generate_possessives import (
    ensure_poss_grammar_forms,
)


class PossessiveRulesTests(TestCase):
    def test_muamo_base(self):
        forms = generate_possessive_forms("muamo", {0: ["muamo"], 1: ["muamo"]})
        self.assertEqual(forms["poss_1sg"], ["muamoni"])
        self.assertEqual(forms["poss_2sg"], ["muamoš"])
        self.assertEqual(forms["poss_dim_1sg"], ["muamozeni"])
        self.assertEqual(forms["poss_dim_2sg"], ["muamozeš"])

    def test_kirjane_ze_stem(self):
        self.assertEqual(build_dim_ze_stem("kirjane"), "kirjaze")
        forms = generate_possessive_forms("kirjane")
        self.assertEqual(forms["poss_1sg"], ["kirjazeni"])
        self.assertEqual(forms["poss_2sg"], ["kirjazeš"])
        self.assertNotIn("poss_dim_1sg", forms)

    def test_pick_prefers_strong_stem(self):
        stem = pick_vowel_stem(
            {0: ["kirveš"], 1: ["kirvehe"], 2: ["kirvehe"]},
            "kirveš",
        )
        self.assertEqual(stem, "kirvehe")
        forms = generate_possessive_forms(
            "kirveš",
            {0: ["kirveš"], 1: ["kirvehe"], 2: ["kirvehe"]},
            include_dim=False,
        )
        self.assertEqual(forms["poss_1sg"], ["kirveheni"])
        self.assertEqual(forms["poss_2sg"], ["kirveheš"])


class PossessiveSearchApiTests(TestCase):
    def setUp(self):
        self.pos_s = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.gf_nom = GrammarForm.objects.create(
            code="nom_sg",
            name_krl="yksikön nominativa",
            name_ru="номинатив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=10,
        )
        ensure_poss_grammar_forms()

        self.muamo = Word(word="muamo", pos=self.pos_s)
        self.muamo.save()
        for n, form in [(0, "muamo"), (1, "muamo"), (2, "muamo")]:
            Stem.objects.create(
                word=self.muamo, number=n, form=form, stem_type=f"noun_{n}"
            )
        WordForm.objects.create(
            word=self.muamo, grammar_form=self.gf_nom, form="muamo"
        )
        gf1 = GrammarForm.objects.get(code="poss_2sg")
        gf_dim = GrammarForm.objects.get(code="poss_dim_1sg")
        WordForm.objects.create(
            word=self.muamo, grammar_form=gf1, form="muamoš"
        )
        WordForm.objects.create(
            word=self.muamo, grammar_form=gf_dim, form="muamozeni"
        )

    def test_search_muamoš(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "muamoš"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["word"], "muamo")
        self.assertEqual(rows[0]["matched_form"], "muamoš")
        labels = rows[0]["matched_form_labels_krl"]
        self.assertTrue(any("omistus" in lab for lab in labels))

    def test_search_muamozeni(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "muamozeni"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(rows[0]["word"], "muamo")
        self.assertTrue(
            any("pieniškö" in lab for lab in rows[0]["matched_form_labels_krl"])
        )

    def test_paradigm_excludes_possessives(self):
        client = APIClient()
        resp = client.get(
            f"/api/v0/lexicon/word-card/{self.muamo.id}/paradigm/"
        )
        self.assertEqual(resp.status_code, 200)
        codes = {row["code"] for row in resp.json()["forms"]}
        self.assertIn("nom_sg", codes)
        self.assertNotIn("poss_2sg", codes)
        forms = " ".join(row["form"] for row in resp.json()["forms"])
        self.assertNotIn("muamoš", forms)
