"""Тесты генератора глаголов фазы 1 (без БД)."""

from django.test import SimpleTestCase

from lexicon.wordform_gen import generate_verb_forms
from lexicon.wordform_gen.rules_verbs import SOFT, cond_imp_3sg


class Cond73FlowchartTests(SimpleTestCase):
    """Блок-схема формы 73."""

    def test_i_not_ua(self):
        # tuli + s'
        self.assertEqual(cond_imp_3sg("tuli", "tulla"), "tuli" + "s" + SOFT)

    def test_i_and_ua(self):
        # otti, ottua → ottais'
        self.assertEqual(cond_imp_3sg("otti", "ottua"), "ottais" + SOFT)

    def test_o_and_ua(self):
        # ando, andua → andais'
        self.assertEqual(cond_imp_3sg("ando", "andua"), "andais" + SOFT)

    def test_not_i_not_ua(self):
        self.assertEqual(cond_imp_3sg("magai", "muata"), "magais" + SOFT)


class AnduaParadigmTests(SimpleTestCase):
    """Эталон Grammatika / Dictorpus dialect=47: andua."""

    STEMS = {
        0: "andua",
        1: "anna",
        2: "anda",
        3: "annoi",
        4: "ando",
        5: "anda",
        6: "anneta",
        7: "annett",
    }

    def test_core(self):
        f = generate_verb_forms(self.STEMS, lemma="andua")
        self.assertEqual(f["inf1"], ["andua"])
        self.assertEqual(f["ind_pres_1sg_pos"], ["annan"])
        self.assertEqual(f["ind_pres_3sg_pos"], ["andau"])
        self.assertEqual(f["ind_pres_3pl_pos"], ["annetah"])
        self.assertEqual(f["ind_impf_3sg_pos"], ["ando"])
        self.assertEqual(f["ind_impf_1pl_pos"], ["andoma"])
        self.assertEqual(f["cond_impf_3sg_pos"], ["andais" + SOFT])
        self.assertEqual(f["cond_impf_1sg_pos"], ["andazin"])
        self.assertEqual(f["cond_impf_3pl_pos"], ["annettais" + SOFT])
        self.assertEqual(f["imp_2sg_pos"], ["anna"])
        self.assertEqual(f["imp_3sg_pos"], ["andakkah"])


class TullaParadigmTests(SimpleTestCase):
    STEMS = {
        0: "tulla",
        1: "tule",
        2: "tule",
        3: "tuli",
        4: "tuli",
        5: "tul",
        6: "tulla",
        7: "tuld",
    }

    def test_present_3sg_e_to_o(self):
        f = generate_verb_forms(self.STEMS, lemma="tulla")
        # Ce → Co + u
        self.assertEqual(f["ind_pres_3sg_pos"], ["tulou"])
        self.assertEqual(f["cond_impf_3sg_pos"], ["tulis" + SOFT])
        self.assertEqual(f["imp_3sg_pos"], ["tulgah"])


class OttuaParadigmTests(SimpleTestCase):
    STEMS = {
        0: "ottua",
        1: "ota",
        2: "otta",
        3: "oti",
        4: "otti",
        5: "otta",
        6: "oteta",
        7: "otett",
    }

    def test_cond73_i_ua(self):
        f = generate_verb_forms(self.STEMS, lemma="ottua")
        self.assertEqual(f["cond_impf_3sg_pos"], ["ottais" + SOFT])
        self.assertEqual(f["cond_impf_1sg_pos"], ["ottazin"])


class AnduaPhase2Tests(SimpleTestCase):
    STEMS = {
        0: "andua",
        1: "anna",
        2: "anda",
        3: "annoi",
        4: "ando",
        5: "anda",
        6: "anneta",
        7: "annett",
    }

    def test_participles(self):
        f = generate_verb_forms(self.STEMS, lemma="andua")
        self.assertEqual(f["part_act1"], ["andaja"])
        self.assertEqual(f["part_act2"], ["andannun"])
        self.assertEqual(f["part_act2_short"], ["andan"])
        self.assertEqual(f["part_pass1"], ["annettava"])
        self.assertEqual(f["part_pass2"], ["annettu"])

    def test_potential_and_inf3(self):
        f = generate_verb_forms(self.STEMS, lemma="andua")
        self.assertEqual(f["pot_pres_1sg_pos"], ["andannen"])
        self.assertEqual(f["pot_pres_3sg_pos"], ["andannou"])
        self.assertEqual(f["pot_pres_3pl_pos"], ["annettanneh"])
        self.assertEqual(f["inf3_ill"], ["andamah"])
        self.assertEqual(f["inf2_iness"], ["anduas" + SOFT + "s" + SOFT + "a"])
        self.assertEqual(f["inf2_instr"], ["anduan"])

    def test_analytic(self):
        f = generate_verb_forms(self.STEMS, lemma="andua")
        self.assertEqual(f["ind_perf_1sg_pos"], ["olen andan"])
        self.assertEqual(f["ind_perf_3sg_pos"], ["on andan"])
        self.assertEqual(f["ind_perf_3pl_pos"], ["on annettu"])
        self.assertEqual(f["ind_impf_1sg_neg"], ["en andan"])
        self.assertEqual(f["ind_plup_3sg_pos"], ["oli andan"])
        self.assertEqual(f["cond_plup_3sg_pos"], [f"olis{SOFT} andan"])
        self.assertEqual(f["pot_perf_1sg_pos"], ["lienen andan"])


class TullaPhase2Tests(SimpleTestCase):
    STEMS = {
        0: "tulla",
        1: "tule",
        2: "tule",
        3: "tuli",
        4: "tuli",
        5: "tul",
        6: "tulla",
        7: "tuld",
    }

    def test_part_l_and_pot(self):
        f = generate_verb_forms(self.STEMS, lemma="tulla")
        self.assertEqual(f["part_act2_short"], ["tullun"])
        self.assertEqual(f["part_act2"], ["tullun"])
        self.assertEqual(f["pot_pres_1sg_pos"], ["tullen"])
        self.assertEqual(f["part_act1"], ["tulija"])  # e→i + ja


class MannaHarmonyTests(SimpleTestCase):
    """män|nä: основа 5 män → nyn (передний ряд)."""

    STEMS = {
        0: "männä",
        1: "mäne",
        2: "mänö",
        3: "mäni",
        4: "mäni",
        5: "män",
        6: "männä",
        7: "mänd",
    }

    def test_part_nyn(self):
        f = generate_verb_forms(self.STEMS, lemma="männä")
        self.assertEqual(f["part_act2"], ["männyn"])
        self.assertEqual(f["part_act2_short"], ["männyn"])
