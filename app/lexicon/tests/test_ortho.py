from django.test import SimpleTestCase

from lexicon.ortho import SOFT_SIGN, normalize_soft_sign, strip_soft_signs


class SoftSignOrthoTests(SimpleTestCase):
    def test_normalize_variants_to_canon(self):
        self.assertEqual(normalize_soft_sign("kir\u2019ja"), f"kir{SOFT_SIGN}ja")
        self.assertEqual(normalize_soft_sign("kir'ja"), f"kir{SOFT_SIGN}ja")
        self.assertEqual(normalize_soft_sign(f"kir{SOFT_SIGN}ja"), f"kir{SOFT_SIGN}ja")

    def test_strip_all_variants(self):
        self.assertEqual(strip_soft_signs("kir\u2019ja"), "kirja")
        self.assertEqual(strip_soft_signs(f"kir{SOFT_SIGN}ja"), "kirja")
        self.assertEqual(strip_soft_signs("kir'ja"), "kirja")
