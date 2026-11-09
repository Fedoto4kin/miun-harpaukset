"""Аналитические словоформы не заливают поиск по префиксу без пробела."""

from django.test import TestCase
from rest_framework.test import APIClient

from lexicon.models import GrammarForm, Pos, Word, WordForm


class WordFormForSearchTests(TestCase):
    def setUp(self):
        self.pos_v = Pos.objects.create(abbr="v.", name_ru="глагол")
        self.gf_neg = GrammarForm.objects.create(
            code="ind_pres_3sg_neg",
            name_krl="indikativa prezens 3.yks. kieltävä",
            name_ru="индикатив презенс 3л. ед. отр.",
            category=GrammarForm.Category.VERB,
            sort_order=180,
        )
        self.gf_pos = GrammarForm.objects.create(
            code="ind_pres_3sg_pos",
            name_krl="indikativa prezens 3.yks. myönteinen",
            name_ru="индикатив презенс 3л. ед. пол.",
            category=GrammarForm.Category.VERB,
            sort_order=80,
        )
        self.ei = Word(word="ei", pos=self.pos_v)
        self.ei.save()
        self.antua = Word(word="antua", pos=self.pos_v)
        self.antua.save()

        WordForm.objects.create(
            word=self.ei, grammar_form=self.gf_pos, form="ei"
        )
        WordForm.objects.create(
            word=self.antua, grammar_form=self.gf_neg, form="ei anna"
        )
        WordForm.objects.create(
            word=self.antua, grammar_form=self.gf_pos, form="antau"
        )

    def test_ei_excludes_analytic_of_other_verbs(self):
        hits = list(WordForm.objects.for_search("ei"))
        self.assertEqual([h.form for h in hits], ["ei"])
        self.assertEqual(hits[0].word_id, self.ei.id)

    def test_space_query_matches_analytic(self):
        hits = list(WordForm.objects.for_search("ei a"))
        self.assertEqual([h.form for h in hits], ["ei anna"])
        self.assertEqual(hits[0].word_id, self.antua.id)

    def test_search_api_ei_returns_lemma_not_antua(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "ei"})
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertIn("ei", words)
        self.assertNotIn("antua", words)

    def test_search_api_form_prefix_not_enough(self):
        """«elä» не должно тянуть eliä через префикс формы elän."""
        self.gf_1sg = GrammarForm.objects.create(
            code="ind_pres_1sg_pos",
            name_krl="indikativa prezens 1.yks. myönteinen",
            name_ru="индикатив презенс 1л. ед. пол.",
            category=GrammarForm.Category.VERB,
            sort_order=60,
        )
        elia = Word(word="eliä", pos=self.pos_v)
        elia.save()
        WordForm.objects.create(
            word=elia, grammar_form=self.gf_1sg, form="elän"
        )

        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "elä"})
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertNotIn("eliä", words)

        resp_exact = client.get("/api/v0/lexicon/search/", {"query": "elän"})
        self.assertEqual(resp_exact.status_code, 200)
        words_exact = {row["word"] for row in resp_exact.json()}
        self.assertIn("eliä", words_exact)

    def test_search_api_lemma_prefix_not_enough(self):
        """«kuin» не должно тянуть kuinbua по префиксу леммы."""
        pos_adv = Pos.objects.create(abbr="adv.", name_ru="наречие")
        kuin = Word(word="kuin", pos=pos_adv)
        kuin.save()
        kuinbua = Word(word="kuinbua", pos=pos_adv)
        kuinbua.save()

        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "kuin"})
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertIn("kuin", words)
        self.assertNotIn("kuinbua", words)
