"""Тесты аудита основ (слой 1 + парсер Dictorpus HTML)."""

from django.test import SimpleTestCase, TestCase

from lexicon.models import GrammarForm, Pos, Stem, Word, WordForm
from lexicon.stem_audit.dictorpus import compare_with_dictorpus, parse_dictorpus_html
from lexicon.stem_audit.normalize import form_key
from lexicon.stem_audit.structural import (
    REASON_ASYMM,
    REASON_EMPTY_WEAK,
    REASON_SUSPECT_GEN,
    audit_word_structural,
    check_asymmetric_gradation,
    check_empty_weak_consonant_stem,
    check_suspect_gen,
)


class StructuralUnitTests(SimpleTestCase):
    def test_asymmetric_rebo_template(self):
        self.assertEqual(
            check_asymmetric_gradation("-v : -bo, -buo, -boloi"),
            "-v : -bo",
        )
        self.assertIsNone(
            check_asymmetric_gradation("-vo : -bo, -buo, -boloi")
        )
        self.assertIsNone(
            check_asymmetric_gradation("-a : -ka, -kua, -oi : -koi")
        )

    def test_suspect_gen_revn(self):
        self.assertTrue(check_suspect_gen("rev", "revn"))
        self.assertFalse(check_suspect_gen("revo", "revon"))
        self.assertFalse(check_suspect_gen("aka", "akan"))

    def test_empty_weak_cuppu(self):
        self.assertEqual(
            check_empty_weak_consonant_stem("- : -pu, -puo, -puloi", "čup"),
            "- : -pu",
        )
        self.assertIsNone(
            check_empty_weak_consonant_stem("- : -pu, -puo, -puloi", "čupu")
        )

    def test_form_key_soft_and_cyr_o(self):
        self.assertEqual(form_key("revоn"), form_key("revon"))
        self.assertEqual(form_key("sʼtʼa"), "sta")


class DictorpusParseTests(SimpleTestCase):
    def test_parse_table_rows(self):
        html = """
        <table><tr><td>1</td><td>revon</td><td>genitive, sg</td></tr>
        <tr><td>2</td><td>rebuo</td><td>partitive, sg</td></tr>
        <tr><td>3</td><td>reboh</td><td>illative, sg</td></tr>
        <tr><td>4</td><td>el&auml;tn</td><td>genitive, sg</td></tr>
        <tr><td>5</td><td>revo&scaron;&scaron;a</td><td>inessive, sg</td></tr></table>
        """
        got = parse_dictorpus_html(html)
        self.assertEqual(got["gen_sg"], {"revon", "elätn"})
        self.assertEqual(got["part_sg"], {"rebuo"})
        self.assertEqual(got["ill_sg"], {"reboh"})
        self.assertEqual(got["iness_sg"], {"revošša"})

    def test_compare_mismatch(self):
        cmp = compare_with_dictorpus(
            {"gen_sg": "revn"},
            {"gen_sg": {"revon"}},
        )
        self.assertFalse(cmp["ok"])
        self.assertIn("gen_sg", cmp["mismatches"])


class StructuralDbTests(TestCase):
    def setUp(self):
        self.pos = Pos.objects.create(abbr="s.", name_ru="существительное")
        self.gf_gen = GrammarForm.objects.create(
            code="gen_sg",
            name_krl="yksikön genetiva",
            name_ru="генитив ед.ч.",
            category=GrammarForm.Category.NOUN,
            sort_order=20,
        )

    def test_flags_bad_rebo_like_word(self):
        w = Word(
            word="re|bo",
            pos=self.pos,
            orig="<p><b>re|bo</b><code>-v : -bo, -buo, -boloi</code><i>s.</i></p>",
        )
        w.save()
        for n, form in [(0, "rebo"), (1, "rev"), (2, "rebo"), (3, "rebuo")]:
            Stem.objects.create(
                word=w, number=n, form=form, stem_type=f"noun_{n}"
            )
        WordForm.objects.create(word=w, grammar_form=self.gf_gen, form="revn")
        w._audit_forms = list(
            WordForm.objects.filter(word=w).select_related("grammar_form")
        )
        row = audit_word_structural(w)
        self.assertIsNotNone(row)
        self.assertIn(REASON_ASYMM, row["reasons"])
        self.assertIn(REASON_SUSPECT_GEN, row["reasons"])
