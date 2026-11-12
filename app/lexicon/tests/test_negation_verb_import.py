"""Тесты таблицы отрицательного глагола ei (без БД)."""

from django.test import SimpleTestCase

from lexicon.negation_verb_import.data import LEMMA, PARADIGM, form_codes, iter_forms


class NegationVerbTableTests(SimpleTestCase):
    def test_lemma(self):
        self.assertEqual(LEMMA, "ei")

    def test_slot_count(self):
        self.assertEqual(len(PARADIGM), 10)
        self.assertEqual(len(list(iter_forms())), 10)
        self.assertEqual(form_codes(), list(PARADIGM.keys()))

    def test_present(self):
        self.assertEqual(PARADIGM["ind_pres_1sg_pos"], "en")
        self.assertEqual(PARADIGM["ind_pres_2sg_pos"], "et")
        self.assertEqual(PARADIGM["ind_pres_3sg_pos"], "ei")
        self.assertEqual(PARADIGM["ind_pres_1pl_pos"], "emmä")
        self.assertEqual(PARADIGM["ind_pres_2pl_pos"], "että")
        self.assertEqual(PARADIGM["ind_pres_3pl_pos"], "ei")

    def test_imperative(self):
        self.assertEqual(PARADIGM["imp_2sg_pos"], "elä")
        self.assertEqual(PARADIGM["imp_3sg_pos"], "elgäh")
        self.assertEqual(PARADIGM["imp_2pl_pos"], "elgiä")
        self.assertEqual(PARADIGM["imp_3pl_pos"], "elgäh")

    def test_no_soft_signs_in_canon(self):
        for code, form in PARADIGM.items():
            self.assertNotIn("ʼ", form, msg=code)
            self.assertNotIn("'", form, msg=code)
