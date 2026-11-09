"""Тесты таблицы местоимений (без БД)."""

from django.test import SimpleTestCase

from lexicon.pronoun_import.data import LEMMAS, PARADIGM, iter_lemma_forms


class PronounTableTests(SimpleTestCase):
    def test_column_alignment(self):
        n = len(LEMMAS)
        for case, forms in PARADIGM.items():
            self.assertEqual(len(forms), n, msg=case)

    def test_nom_equals_lemma(self):
        for (lemma, _num), form in zip(LEMMAS, PARADIGM["nom"]):
            self.assertEqual(lemma, form)

    def test_mie_core(self):
        by_code = {
            code: form
            for lemma, _n, code, form in iter_lemma_forms()
            if lemma == "mie"
        }
        self.assertEqual(by_code["nom_sg"], "mie")
        self.assertEqual(by_code["gen_sg"], "miun")
        self.assertEqual(by_code["part_sg"], "miut")
        self.assertEqual(by_code["acc_sg"], "milma")
        self.assertEqual(by_code["iness_sg"], "miušša")
        self.assertEqual(by_code["ill_sg"], "miuh")

    def test_myo_uses_pl_codes(self):
        codes = {
            code
            for lemma, _n, code, _f in iter_lemma_forms()
            if lemma == "myö"
        }
        self.assertIn("nom_pl", codes)
        self.assertIn("acc_pl", codes)
        self.assertNotIn("nom_sg", codes)

    def test_slot_count(self):
        # 12 lemmas × 13 cases
        self.assertEqual(len(list(iter_lemma_forms())), 12 * 13)
