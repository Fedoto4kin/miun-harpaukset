"""Продуктивные уменьшительные s. на -ne: поиск-цепочка, не в парадигме."""

from django.test import TestCase
from rest_framework.test import APIClient

from lexicon.models import GrammarForm, Pos, Stem, Word, WordForm
from lexicon.wordform_gen.diminutives import (
    build_diminutive_stems,
    generate_diminutive_forms,
)
from lexicon.management.commands.generate_diminutives import (
    ensure_dim_grammar_forms,
)


class DiminutiveStemRulesTests(TestCase):
    def test_peldo_stems_and_key_forms(self):
        stems = build_diminutive_stems("peldo")
        self.assertEqual(stems[0], "peldone")
        self.assertEqual(stems[1], "peldoze")
        self.assertEqual(stems[3], "peldosʼtʼa")
        self.assertEqual(stems[4], "peldozi")

        forms = generate_diminutive_forms("peldo")
        self.assertEqual(forms["nom_sg"], ["peldone"])
        self.assertEqual(forms["gen_sg"], ["peldozen"])
        self.assertEqual(forms["elat_sg"], ["peldozešta"])
        self.assertEqual(forms["ill_sg"], ["peldozeh"])
        self.assertEqual(forms["elat_pl"], ["peldozista"])

    def test_skip_already_ne(self):
        self.assertIsNone(build_diminutive_stems("alane"))
        self.assertEqual(generate_diminutive_forms("kirjane"), {})


class DiminutiveSearchApiTests(TestCase):
    def setUp(self):
        self.pos_s = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.gf_nom = GrammarForm.objects.create(
            code="nom_sg",
            name_krl="yksikön nominativa",
            name_ru="номинатив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=10,
        )
        self.gf_elat = GrammarForm.objects.create(
            code="elat_sg",
            name_krl="yksikön elativa",
            name_ru="элатив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=70,
        )
        ensure_dim_grammar_forms()

        self.peldo = Word(word="pel|do", pos=self.pos_s)
        self.peldo.save()
        for n, form in [
            (0, "peldo"),
            (1, "pello"),
            (2, "peldo"),
            (3, "pelduo"),
            (4, "peldoloi"),
            (5, "peldoloi"),
        ]:
            Stem.objects.create(
                word=self.peldo, number=n, form=form, stem_type=f"noun_{n}"
            )
        WordForm.objects.create(
            word=self.peldo, grammar_form=self.gf_nom, form="peldo"
        )
        WordForm.objects.create(
            word=self.peldo, grammar_form=self.gf_elat, form="pellošta"
        )

        # Продуктивные dim-формы (как generate_diminutives)
        gf_dim_elat = GrammarForm.objects.get(code="dim_elat_sg")
        gf_dim_nom = GrammarForm.objects.get(code="dim_nom_sg")
        WordForm.objects.create(
            word=self.peldo, grammar_form=gf_dim_nom, form="peldone"
        )
        WordForm.objects.create(
            word=self.peldo, grammar_form=gf_dim_elat, form="peldozešta"
        )

        # Sibling *ne — kirja/kirjane: база не должна получать dim
        self.kirja = Word(word="kirj|a", pos=self.pos_s)
        self.kirja.save()
        self.kirjane = Word(word="kirja|ne", pos=self.pos_s)
        self.kirjane.save()

    def test_search_peldozešta_chains_to_peldo(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "peldozešta"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["word"], "pel|do")
        self.assertEqual(rows[0]["matched_form"], "peldozešta")
        labels = rows[0]["matched_form_labels_krl"]
        self.assertTrue(any("pieniškö" in lab for lab in labels))

    def test_suggestions_chain(self):
        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/",
            {"query": "peldozešta"},
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == self.peldo.id]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_form"], "peldozešta")

    def test_paradigm_excludes_diminutives(self):
        client = APIClient()
        resp = client.get(
            f"/api/v0/lexicon/word-card/{self.peldo.id}/paradigm/"
        )
        self.assertEqual(resp.status_code, 200)
        codes = {row["code"] for row in resp.json()["forms"]}
        self.assertIn("nom_sg", codes)
        self.assertIn("elat_sg", codes)
        self.assertNotIn("dim_elat_sg", codes)
        self.assertNotIn("dim_nom_sg", codes)
        forms = " ".join(row["form"] for row in resp.json()["forms"])
        self.assertNotIn("peldozešta", forms)
        self.assertNotIn("peldone", forms)
