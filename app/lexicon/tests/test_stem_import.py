"""Unit-тесты одноразового парсера основ (без БД)."""

from django.test import SimpleTestCase

from lexicon.stem_import import build_stems, parse_orig
from lexicon.stem_import.build_stems import (
    apply_suffix,
    lemma_clean,
    parse_template_slots,
    stem_base,
)


class ParseOrigTests(SimpleTestCase):
    def test_noun_simple(self):
        orig = (
            "<p><b>abie</b><code>-, -da, -loi</code> "
            "<i>a.</i><mark> грустный – surullinen</mark></p>"
        )
        p = parse_orig(orig)
        self.assertEqual(p.lemma, "abie")
        self.assertEqual(p.code, "-, -da, -loi")
        self.assertEqual(p.pos_abbr, "a.")
        self.assertEqual(p.special_mark, "")

    def test_noun_gradation(self):
        orig = (
            "<p><b>a|bu</b> <code>-vu : -bu, -buo, -vuloi : -buloi</code> "
            "<i>s.</i><mark> помощь – apu</mark></p>"
        )
        p = parse_orig(orig)
        self.assertEqual(p.lemma, "a|bu")
        self.assertEqual(p.code, "-vu : -bu, -buo, -vuloi : -buloi")
        self.assertEqual(p.pos_abbr, "s.")

    def test_verb_full(self):
        orig = (
            "<p><b>ahavoit|tua</b> <code>-a : -ta, -i : -ti, -ta, -eta, -ett</code> "
            "<i>v.</i><mark> обветрить – kuivattaa</mark></p>"
        )
        p = parse_orig(orig)
        self.assertEqual(p.lemma, "ahavoit|tua")
        self.assertEqual(p.pos_abbr, "v.")
        self.assertEqual(p.special_mark, "")

    def test_pl_mark_in_italic(self):
        orig = (
            "<p><b>aluššo|vat</b> <code>-vi : -bi</code> "
            "<i>s. pl.</i><mark> нижнее белье</mark></p>"
        )
        p = parse_orig(orig)
        self.assertEqual(p.pos_abbr, "s.")
        self.assertEqual(p.special_mark, "pl")

    def test_v_def_mark(self):
        orig = (
            "<p><b>avau|duo</b> <code>-du, -du, -du, -vuta, -vutt</code> "
            "<i>v. def.</i><mark> открываться</mark></p>"
        )
        p = parse_orig(orig)
        self.assertEqual(p.pos_abbr, "v.")
        self.assertEqual(p.special_mark, "v_def")

    def test_sing_mark(self):
        orig = (
            "<p><b>Kariel|a</b> <code>-a, -ua</code> "
            "<i>s. sing.</i><mark>Карелия</mark></p>"
        )
        p = parse_orig(orig)
        self.assertEqual(p.special_mark, "sing")
        self.assertEqual(p.pos_abbr, "s.")

    def test_no_code_adverb(self):
        orig = "<p><b>alah</b><i>adv.</i><mark> вниз – alas</mark></p>"
        p = parse_orig(orig)
        self.assertEqual(p.lemma, "alah")
        self.assertIsNone(p.code)
        self.assertEqual(p.pos_abbr, "adv.")

    def test_empty(self):
        p = parse_orig("")
        self.assertEqual(p.lemma, "")
        self.assertIsNone(p.code)


class StemBaseTests(SimpleTestCase):
    def test_with_pipe(self):
        self.assertEqual(stem_base("ak|ka"), "ak")
        self.assertEqual(lemma_clean("ak|ka"), "akka")

    def test_without_pipe(self):
        self.assertEqual(stem_base("abie"), "abie")
        self.assertEqual(lemma_clean("abie"), "abie")

    def test_apply_suffix(self):
        self.assertEqual(apply_suffix("ak", "-"), "ak")
        self.assertEqual(apply_suffix("ak", "-a"), "aka")
        self.assertEqual(apply_suffix("ak", "-ka"), "akka")


class ParseTemplateSlotsTests(SimpleTestCase):
    def test_simple_noun(self):
        slots = parse_template_slots("-, -da, -loi")
        self.assertEqual(
            slots,
            [[("-", None)], [("-da", None)], [("-loi", None)]],
        )

    def test_gradation_colon(self):
        slots = parse_template_slots("-vu : -bu, -buo, -vuloi : -buloi")
        self.assertEqual(
            slots,
            [[("-vu", "-bu")], [("-buo", None)], [("-vuloi", "-buloi")]],
        )

    def test_gradation_semicolon(self):
        slots = parse_template_slots("-a ; -ta, -tua, -oi : -toi")
        self.assertEqual(
            slots,
            [[("-a", "-ta")], [("-tua", None)], [("-oi", "-toi")]],
        )

    def test_slash_alternatives(self):
        slots = parse_template_slots("-je : -de, -ttä, -zi / -zilöi")
        self.assertEqual(
            slots,
            [
                [("-je", "-de")],
                [("-ttä", None)],
                [("-zi", None), ("-zilöi", None)],
            ],
        )


class BuildNominalStemsTests(SimpleTestCase):
    def test_abie(self):
        stems = build_stems("abie", "-, -da, -loi", "a.")
        self.assertEqual(
            stems,
            {
                0: ["abie"],
                1: ["abie"],
                2: ["abie"],
                3: ["abieda"],
                4: ["abieloi"],
                5: ["abieloi"],
            },
        )

    def test_abu(self):
        stems = build_stems(
            "a|bu", "-vu : -bu, -buo, -vuloi : -buloi", "s."
        )
        self.assertEqual(
            stems,
            {
                0: ["abu"],
                1: ["avu"],
                2: ["abu"],
                3: ["abuo"],
                4: ["avuloi"],
                5: ["abuloi"],
            },
        )

    def test_rebo_stem1_override(self):
        # Словарь: -v : -bo; без оверрайда → rev/revn, нужно revo/revon.
        stems = build_stems("re|bo", "-v : -bo, -buo, -boloi", "s.")
        self.assertEqual(stems[1], ["revo"])
        self.assertEqual(stems[2], ["rebo"])
        self.assertEqual(stems[3], ["rebuo"])

    def test_akka(self):
        stems = build_stems("ak|ka", "-a : -ka, -kua, -oi : -koi", "s.")
        self.assertEqual(
            stems,
            {
                0: ["akka"],
                1: ["aka"],
                2: ["akka"],
                3: ["akkua"],
                4: ["akoi"],
                5: ["akkoi"],
            },
        )

    def test_pl_only(self):
        stems = build_stems("aluššo|vat", "-vi : -bi", "s.", special_mark="pl")
        self.assertEqual(stems[0], ["aluššovat"])
        self.assertEqual(stems[4], ["aluššovi"])
        self.assertEqual(stems[5], ["aluššobi"])
        self.assertNotIn(1, stems)
        self.assertNotIn(3, stems)

    def test_sing_only(self):
        stems = build_stems("Kariel|a", "-a, -ua", "s.", special_mark="sing")
        self.assertEqual(
            stems,
            {
                0: ["Kariela"],
                1: ["Kariela"],
                2: ["Kariela"],
                3: ["Karielua"],
            },
        )
        self.assertNotIn(4, stems)

    def test_vezi_alternatives(self):
        stems = build_stems(
            "ve|zi", "-je : -de, -ttä, -zi / -zilöi", "s."
        )
        self.assertEqual(stems[1], ["veje"])
        self.assertEqual(stems[2], ["vede"])
        self.assertEqual(stems[3], ["vettä"])
        self.assertEqual(stems[4], ["vezi", "vezilöi"])
        self.assertEqual(stems[5], ["vezi", "vezilöi"])

    def test_pron_nominal_and_ken_override(self):
        # Глоссарий Novak: ken (kenen, kedä)
        stems = build_stems("ke|n", "-, -dä", "pron.", special_mark="sing")
        self.assertEqual(stems[0], ["ken"])
        self.assertEqual(stems[1], ["kene"])
        self.assertEqual(stems[2], ["kene"])
        self.assertEqual(stems[3], ["kedä"])

    def test_mi_book_override_ignores_pl_mark(self):
        # orig: pron. pl.; глосс: mi (min, midä)
        stems = build_stems("mi", "-, -dä", "pron.", special_mark="pl")
        self.assertEqual(stems[1], ["mi"])
        self.assertEqual(stems[3], ["midä"])
        self.assertNotIn(4, stems)

    def test_book_overrides_se_moni_kumbane(self):
        še = build_stems("š|e", "-i, -dä", "pron.", special_mark="sing")
        self.assertEqual(še[1], ["še"])
        self.assertEqual(še[3], ["šidä"])
        moni = build_stems("mon|i", "-e, -da, -i", "pron.")
        self.assertEqual(moni[3], ["monie"])
        kum = build_stems("kum|bane", "-baze, -masʼtʼa, -bazi", "pron.")
        self.assertEqual(kum[1], ["kumbeze"])

    def test_soft_sign_canon_in_suffix(self):
        from lexicon.ortho import SOFT_SIGN

        # U+2019 в шаблоне → U+02BC в основе
        code = "-ze, -s\u2019t\u2019a, -zi"
        stems = build_stems("pala|ne", code, "s.")
        self.assertIn(SOFT_SIGN, stems[3][0])
        self.assertNotIn("\u2019", stems[3][0])


class BuildVerbStemsTests(SimpleTestCase):
    def test_ahavoittua(self):
        stems = build_stems(
            "ahavoit|tua",
            "-a : -ta, -i : -ti, -ta, -eta, -ett",
            "v.",
        )
        self.assertEqual(
            stems,
            {
                0: ["ahavoittua"],
                1: ["ahavoita"],
                2: ["ahavoitta"],
                3: ["ahavoiti"],
                4: ["ahavoitti"],
                5: ["ahavoitta"],
                6: ["ahavoiteta"],
                7: ["ahavoitett"],
            },
        )

    def test_verb_without_gradation(self):
        stems = build_stems("aj|ua", "-a, -oi, -a, -eta, -ett", "v.")
        self.assertEqual(stems[1], ["aja"])
        self.assertEqual(stems[2], ["aja"])
        self.assertEqual(stems[3], ["ajoi"])
        self.assertEqual(stems[4], ["ajoi"])
        self.assertEqual(stems[5], ["aja"])
        self.assertEqual(stems[6], ["ajeta"])
        self.assertEqual(stems[7], ["ajett"])

    def test_v_def(self):
        stems = build_stems(
            "avau|duo",
            "-du, -du, -du, -vuta, -vutt",
            "v.",
            special_mark="v_def",
        )
        self.assertEqual(stems[0], ["avauduo"])
        self.assertEqual(stems[2], ["avaudu"])
        self.assertEqual(stems[4], ["avaudu"])
        self.assertEqual(stems[5], ["avaudu"])
        self.assertEqual(stems[6], ["avauvuta"])
        self.assertEqual(stems[7], ["avauvutt"])
        self.assertNotIn(1, stems)
        self.assertNotIn(3, stems)

    def test_end_to_end_from_orig(self):
        orig = (
            "<p><b>ak|ka</b> <code>-a : -ka, -kua, -oi : -koi</code> "
            "<i>s.</i><mark> старуха</mark></p>"
        )
        p = parse_orig(orig)
        stems = build_stems(p.lemma, p.code, p.pos_abbr, p.special_mark)
        self.assertEqual(stems[2], ["akka"])
        self.assertEqual(stems[5], ["akkoi"])
