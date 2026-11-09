"""Тесты генератора именных словоформ (без БД)."""

from django.test import SimpleTestCase

from lexicon.wordform_gen import generate_adj_forms, generate_noun_forms
from lexicon.wordform_gen.harmony import is_back_harmony, pick


class HarmonyTests(SimpleTestCase):
    def test_back(self):
        self.assertTrue(is_back_harmony("aka"))
        self.assertEqual(pick("aka", "lla", "llä"), "lla")

    def test_front(self):
        self.assertFalse(is_back_harmony("emännä"))
        self.assertEqual(pick("emännä", "lla", "llä"), "llä")


class AkkaParadigmTests(SimpleTestCase):
    """Gold set из Dictorpus: lemma=akka, dialect=47."""

    STEMS = {0: "akka", 1: "aka", 2: "akka", 3: "akkua", 4: "akoi", 5: "akkoi"}

    EXPECTED = {
        "nom_sg": ["akka"],
        "gen_sg": ["akan"],
        "part_sg": ["akkua"],
        "ess_sg": ["akkana"],
        "transl_sg": ["akakši"],
        "iness_sg": ["akašša"],
        "elat_sg": ["akašta"],
        "ill_sg": ["akkah"],
        "ades_sg": ["akalla"],
        "ablat_sg": ["akalda"],
        "abess_sg": ["akatta"],
        "com_sg": ["akanke"],
        "prol_sg": ["akačči"],
        "nom_pl": ["akat"],
        "gen_pl": ["akoin"],
        "part_pl": ["akkoida"],
        "ess_pl": ["akkoina"],
        "transl_pl": ["akoiksi"],
        "iness_pl": ["akoissa"],
        "elat_pl": ["akoista"],
        "ill_pl": ["akkoih"],
        "ades_pl": ["akoilla"],
        "ablat_pl": ["akoilda"],
        "abess_pl": ["akoitta"],
        "com_pl": ["akoinke"],
        "prol_pl": ["akoičči"],
        "instr_pl": ["akoin"],
    }

    def test_full_paradigm(self):
        forms = generate_noun_forms(self.STEMS)
        self.assertEqual(forms, self.EXPECTED)

    def test_sing_mark(self):
        forms = generate_noun_forms(self.STEMS, special_mark="sing")
        self.assertIn("nom_sg", forms)
        self.assertNotIn("nom_pl", forms)

    def test_pl_mark(self):
        forms = generate_noun_forms(self.STEMS, special_mark="pl")
        self.assertIn("nom_pl", forms)
        self.assertNotIn("nom_sg", forms)


class AbuParadigmSmokeTests(SimpleTestCase):
    STEMS = {0: "abu", 1: "avu", 2: "abu", 3: "abuo", 4: "avuloi", 5: "abuloi"}

    def test_core_cases(self):
        forms = generate_noun_forms(self.STEMS)
        self.assertEqual(forms["nom_sg"], ["abu"])
        self.assertEqual(forms["gen_sg"], ["avun"])
        self.assertEqual(forms["part_sg"], ["abuo"])
        self.assertEqual(forms["ill_sg"], ["abuh"])
        self.assertEqual(forms["nom_pl"], ["avut"])
        self.assertEqual(forms["gen_pl"], ["avuloin"])
        self.assertEqual(forms["part_pl"], ["abuloida"])
        self.assertEqual(forms["ill_pl"], ["abuloih"])


class VeziAlternativesTests(SimpleTestCase):
    """Две парадигмы мн.ч. из шаблона -zi / -zilöi (Dictorpus dialect=47)."""

    STEMS = {
        0: ["vezi"],
        1: ["veje"],
        2: ["vede"],
        3: ["vettä"],
        4: ["vezi", "vezilöi"],
        5: ["vezi", "vezilöi"],
    }

    def test_sg_unchanged(self):
        forms = generate_noun_forms(self.STEMS)
        self.assertEqual(forms["nom_sg"], ["vezi"])
        self.assertEqual(forms["gen_sg"], ["vejen"])
        self.assertEqual(forms["iness_sg"], ["veješšä"])
        self.assertEqual(forms["ill_sg"], ["vedeh"])

    def test_pl_both_alts(self):
        forms = generate_noun_forms(self.STEMS)
        self.assertEqual(forms["gen_pl"], ["vezin", "vezilöin"])
        self.assertEqual(forms["part_pl"], ["vezie", "vezilöidä"])
        self.assertEqual(forms["ill_pl"], ["vezih", "vezilöih"])
        self.assertEqual(forms["nom_pl"], ["vejet"])


class ShogieAdjectiveTests(SimpleTestCase):
    """Gold set Dictorpus: lemma=šogie, dialect=47, прилагательное."""

    STEMS = {
        0: "šogie",
        1: "šogie",
        2: "šogie",
        3: "šogieda",
        4: "šogieloi",
        5: "šogieloi",
    }

    def test_alias_same_as_noun(self):
        self.assertEqual(
            generate_adj_forms(self.STEMS),
            generate_noun_forms(self.STEMS),
        )

    def test_core_cases(self):
        forms = generate_adj_forms(self.STEMS)
        self.assertEqual(forms["nom_sg"], ["šogie"])
        self.assertEqual(forms["gen_sg"], ["šogien"])
        self.assertEqual(forms["part_sg"], ["šogieda"])
        self.assertEqual(forms["ess_sg"], ["šogiena"])
        self.assertEqual(forms["transl_sg"], ["šogiekši"])
        self.assertEqual(forms["iness_sg"], ["šogiešša"])
        self.assertEqual(forms["elat_sg"], ["šogiešta"])
        self.assertEqual(forms["ill_sg"], ["šogieh"])
        self.assertEqual(forms["ades_sg"], ["šogiella"])
        self.assertEqual(forms["ablat_sg"], ["šogielda"])
        self.assertEqual(forms["abess_sg"], ["šogietta"])
        self.assertEqual(forms["com_sg"], ["šogienke"])
        self.assertEqual(forms["prol_sg"], ["šogiečči"])
        self.assertEqual(forms["nom_pl"], ["šogiet"])
        self.assertEqual(forms["gen_pl"], ["šogieloin"])
        self.assertEqual(forms["part_pl"], ["šogieloida"])
        self.assertEqual(forms["ill_pl"], ["šogieloih"])
        self.assertEqual(forms["instr_pl"], ["šogieloin"])
