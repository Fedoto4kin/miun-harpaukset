from django.test import SimpleTestCase, TestCase

from lexicon.models import KRL_ABC, Pos, Word


class WordSearchPrepareTests(SimpleTestCase):
    def test_search_prepare_alphabet_and_umlaut(self):
        search = "ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖüÜ'’"
        self.assertEqual(Word.search_prepare(search), "abcčdefghijklmnoprsšzžtuvyäöyy")

    def test_search_prepare_lowercases(self):
        self.assertEqual(Word.search_prepare("AkKa"), "akka")

    def test_search_prepare_strips_apostrophes(self):
        self.assertEqual(Word.search_prepare("kir’ja"), "kirja")
        self.assertEqual(Word.search_prepare("kir'ja"), "kirja")

    def test_search_prepare_empty(self):
        self.assertEqual(Word.search_prepare(""), "")

    def test_search_prepare_keeps_pipe(self):
        # search_prepare does not strip morpheme boundary; word_clean does
        self.assertEqual(Word.search_prepare("ak|ka"), "ak|ka")


class WordSlugifyTests(SimpleTestCase):
    def test_krl_slugify_filters_to_alphabet(self):
        word = Word(word="ak|ka!")
        self.assertEqual(word.krl_slugify(), "akka")

    def test_krl_slugify_umlaut_to_y(self):
        # Only ü→y; ö is in KRL_ABC and kept.
        word = Word(word="tüö")
        self.assertEqual(word.krl_slugify(), "työ")

    def test_krl_slugify_keeps_karelian_letters(self):
        word = Word(word="Šana")
        self.assertEqual(word.krl_slugify(), "šana")
        self.assertTrue(set(KRL_ABC.lower()).issuperset(set("šana")))


class WordCleanSaveTests(TestCase):
    def setUp(self):
        self.pos = Pos.objects.create(abbr="s.", name_ru="существительное")

    def test_save_strips_pipe_and_apostrophes(self):
        word = Word(word="ak|ka", pos=self.pos)
        word.save()
        self.assertEqual(word.word_clean, "akka")

        word.word = "kir’ja"
        word.save()
        self.assertEqual(word.word_clean, "kirja")

        word.word = "kir'ja"
        word.save()
        self.assertEqual(word.word_clean, "kirja")

    def test_save_preserves_case_in_word_clean(self):
        word = Word(word="Ak|Ka", pos=self.pos)
        word.save()
        self.assertEqual(word.word_clean, "AkKa")
