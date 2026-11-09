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


class HomonymWordformDisplayTests(TestCase):
    def setUp(self):
        self.pos_s = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.pos_adv = Pos.objects.create(abbr="adv.", name_ru="наречие")
        self.pos_conj = Pos.objects.create(abbr="conj.", name_ru="союз")
        self.gf_gen = GrammarForm.objects.create(
            code="gen_sg",
            name_krl="genetiiva yks.",
            name_ru="генитив ед.",
            category=GrammarForm.Category.NOUN,
            sort_order=10,
        )
        self.gf_instr = GrammarForm.objects.create(
            code="instr_pl",
            name_krl="instruktiiva mon.",
            name_ru="инструктив мн.",
            category=GrammarForm.Category.NOUN,
            sort_order=20,
        )

    def test_search_joins_multi_slot_labels(self):
        word = Word(word="talo", pos=self.pos_s)
        word.save()
        WordForm.objects.create(word=word, grammar_form=self.gf_gen, form="taloin")
        WordForm.objects.create(word=word, grammar_form=self.gf_instr, form="taloin")

        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "taloin"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_form"], "taloin")
        self.assertEqual(
            rows[0]["matched_form_labels_krl"],
            ["genetiiva yks.", "instruktiiva mon."],
        )

    def test_suggestions_keep_same_lemma_different_pos(self):
        w_adv = Word(word="kuin", pos=self.pos_adv)
        w_adv.save()
        w_conj = Word(word="kuin", pos=self.pos_conj)
        w_conj.save()

        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/", {"query": "kuin"}
        )
        self.assertEqual(resp.status_code, 200)
        ids = {row["word_id"] for row in resp.json()}
        self.assertIn(w_adv.id, ids)
        self.assertIn(w_conj.id, ids)

    def test_suggestions_join_multi_slot_labels(self):
        word = Word(word="talo", pos=self.pos_s)
        word.save()
        WordForm.objects.create(word=word, grammar_form=self.gf_gen, form="taloin")
        WordForm.objects.create(word=word, grammar_form=self.gf_instr, form="taloin")

        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/", {"query": "taloin"}
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == word.id]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_form"], "taloin")
        self.assertEqual(
            rows[0]["matched_form_labels_krl"],
            ["genetiiva yks.", "instruktiiva mon."],
        )


class LetterBrowseTests(TestCase):
    """Алфавитная лента — префикс по лемме, не exact-search."""

    def setUp(self):
        self.pos = Pos.objects.create(abbr="s.", name_ru="существительное")
        for w in ("akka", "abu", "kala"):
            Word(word=w, pos=self.pos).save()

    def test_letter_lists_prefix_lemmas(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"letter": "a"})
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertEqual(words, {"akka", "abu"})

    def test_query_a_is_exact_not_letter(self):
        """?query=a больше не тянет всю букву A."""
        Word(word="a", pos=self.pos).save()
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "a"})
        self.assertEqual(resp.status_code, 200)
        words = {row["word"] for row in resp.json()}
        self.assertEqual(words, {"a"})


class AltSpellingSearchTests(TestCase):
    """Песенные/разговорные альты — поиск, канон в парадигме не меняется."""

    def setUp(self):
        self.pos_v = Pos.objects.create(abbr="v.", name_ru="глагол")
        self.gf_impf = GrammarForm.objects.create(
            code="ind_impf_1sg_pos",
            name_krl="indikativa imperfekta 1.yks. myönteinen",
            name_ru="индикатив имперфект 1л. ед. пол.",
            category=GrammarForm.Category.VERB,
            sort_order=220,
        )
        self.word = Word(word="käyvä", pos=self.pos_v)
        self.word.save()
        self.wf = WordForm(
            word=self.word,
            grammar_form=self.gf_impf,
            form="kävyin",
            alt_spellings=["kävin"],
        )
        self.wf.save()

    def test_exact_search_via_alt(self):
        client = APIClient()
        resp = client.get("/api/v0/lexicon/search/", {"query": "kävin"})
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["word"], "käyvä")
        self.assertEqual(rows[0]["matched_form"], "kävin")
        self.assertEqual(
            rows[0]["matched_form_labels_krl"],
            ["indikativa imperfekta 1.yks. myönteinen"],
        )

    def test_suggestions_via_alt(self):
        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/", {"query": "kävin"}
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == self.word.id]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_form"], "kävin")

    def test_canon_unchanged(self):
        self.assertEqual(self.wf.form, "kävyin")
        self.assertEqual(self.wf.alt_spellings, ["kävin"])
        self.assertEqual(self.wf.alt_spellings_clean, ["kävin"])


class PrefixFormSuggestionDiversityTests(TestCase):
    """aka → чипы akan/akašta/…, не одна цепочка akan→akka."""

    def setUp(self):
        self.pos_s = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.word = Word(word="ak|ka", pos=self.pos_s)
        self.word.save()
        slots = [
            ("gen_sg", "akan", "genetiiva yks."),
            ("elat_sg", "akašta", "elatiiva yks."),
            ("com_sg", "akanke", "komitatiiva yks."),
            ("iness_sg", "akašša", "inessiiva yks."),
        ]
        for i, (code, form, name) in enumerate(slots):
            gf = GrammarForm.objects.create(
                code=code,
                name_krl=name,
                name_ru=name,
                category=GrammarForm.Category.NOUN,
                sort_order=10 + i,
            )
            WordForm.objects.create(word=self.word, grammar_form=gf, form=form)

    def test_prefix_aka_shows_diverse_sample_forms(self):
        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/", {"query": "aka"}
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == self.word.id]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertNotIn("matched_form", row)
        forms = {sf["form"] for sf in row.get("sample_forms", [])}
        self.assertIn("akan", forms)
        self.assertIn("akašta", forms)
        self.assertIn("akanke", forms)

    def test_akan_keeps_longer_siblings_as_chips(self):
        """akan точно есть, но akanke тоже на префиксе — чипы, не одна цепочка."""
        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/", {"query": "akan"}
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == self.word.id]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertNotIn("matched_form", row)
        forms = {sf["form"] for sf in row.get("sample_forms", [])}
        self.assertIn("akan", forms)
        self.assertIn("akanke", forms)

    def test_unique_exact_form_still_chain(self):
        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/", {"query": "akašta"}
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == self.word.id]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_form"], "akašta")
        self.assertNotIn("sample_forms", rows[0])

    def test_unique_prefix_shows_chain_immediately(self):
        """Неполный префикс одной формы → сразу цепочка, не чип."""
        w2 = Word(word="pel|do", pos=self.pos_s)
        w2.save()
        WordForm.objects.create(
            word=w2,
            grammar_form=GrammarForm.objects.get(code="elat_sg"),
            form="peldozešta",
        )
        client = APIClient()
        resp = client.get(
            "/api/v0/lexicon/grouped-search-suggestions/",
            {"query": "peldozešt"},
        )
        self.assertEqual(resp.status_code, 200)
        rows = [r for r in resp.json() if r.get("word_id") == w2.id]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["matched_form"], "peldozešta")
        self.assertNotIn("sample_forms", rows[0])
