"""Сравнительная степень -mbi: поиск-цепочка, не в парадигме."""

from django.test import TestCase
from rest_framework.test import APIClient

from lexicon.models import GrammarForm, Pos, Stem, Word, WordForm
from lexicon.wordform_gen.comparatives import (
    build_comparative_nom,
    generate_comparative_forms,
)
from lexicon.management.commands.generate_comparatives import (
    ensure_comp_grammar_forms,
)


class ComparativeRulesTests(TestCase):
    def test_soma_a_to_e(self):
        self.assertEqual(
            build_comparative_nom("šoma", {0: ["šoma"], 1: ["šoma"]}),
            "šomembi",
        )

    def test_pieni_stem_e(self):
        self.assertEqual(
            build_comparative_nom("pieni", {0: ["pieni"], 1: ["piene"]}),
            "pienembi",
        )

    def test_nuori_nom_heuristic(self):
        self.assertEqual(build_comparative_nom("nuori"), "nuorembi")

    def test_korgie_ie(self):
        self.assertEqual(
            build_comparative_nom("korgie", {1: ["korgie"]}),
            "korgiembi",
        )

    def test_armas_stem(self):
        self.assertEqual(
            build_comparative_nom(
                "armaš", {0: ["armaš"], 1: ["armahe"], 2: ["armahe"]}
            ),
            "armahembi",
        )

    def test_syva(self):
        self.assertEqual(
            build_comparative_nom("šyvä", {1: ["šyvä"]}),
            "šyvembi",
        )

    def test_lambima(self):
        self.assertEqual(
            build_comparative_nom("lämbimä", {1: ["lämbimä"]}),
            "lämbimembi",
        )

    def test_hyva_suppletive_skip(self):
        self.assertIsNone(build_comparative_nom("hyvä", {1: ["hyvä"]}))
        self.assertEqual(generate_comparative_forms("hyvä"), {})

    def test_already_mbi_skip(self):
        self.assertIsNone(build_comparative_nom("parembi"))


class ComparativeSearchApiTests(TestCase):
    def setUp(self):
        self.pos_a = Pos.objects.create(abbr="a.", name_ru="прилагательное")
        self.gf_nom = GrammarForm.objects.create(
            code="nom_sg",
            name_krl="yksikön nominativa",
            name_ru="номинатив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=10,
        )
        ensure_comp_grammar_forms()

        self.nuori = Word(word="nuori", pos=self.pos_a)
        self.nuori.save()
        for n, form in [(0, "nuori"), (1, "nuore"), (2, "nuore")]:
            Stem.objects.create(
                word=self.nuori, number=n, form=form, stem_type=f"noun_{n}"
            )
        WordForm.objects.create(
            word=self.nuori, grammar_form=self.gf_nom, form="nuori"
        )
        gf_comp = GrammarForm.objects.get(code="comp")
        WordForm.objects.create(
            word=self.nuori, grammar_form=gf_comp, form="nuorembi"
        )

    def test_search_nuorembi(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "nuorembi"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["word"], "nuori")
        self.assertEqual(rows[0]["matched_form"], "nuorembi")
        labels = rows[0]["matched_form_labels_krl"]
        self.assertTrue(any("komparativa" in lab for lab in labels))

    def test_paradigm_excludes_comparative(self):
        client = APIClient()
        resp = client.get(
            f"/api/v0/lexicon/word-card/{self.nuori.id}/paradigm/"
        )
        self.assertEqual(resp.status_code, 200)
        codes = {row["code"] for row in resp.json()["forms"]}
        self.assertIn("nom_sg", codes)
        self.assertNotIn("comp", codes)
        forms = " ".join(row["form"] for row in resp.json()["forms"])
        self.assertNotIn("nuorembi", forms)
