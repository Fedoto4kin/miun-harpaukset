"""
Разово генерирует WordForm из Stem по правилам Grammatika.

Генератор: lexicon.wordform_gen (не runtime).
s./a./pron. — именная парадигма; v. — глаголы (фазы 1–2).
pron.: пропускает леммы из Mestoimenia (готовые таблицы, category=pron).
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from lexicon.models import GrammarForm, Word, WordForm
from lexicon.ortho import normalize_soft_sign
from lexicon.pronoun_import.data import INDECLINABLE_LEMMAS
from lexicon.pronoun_import.data import LEMMAS as PERSONAL_PRONOUN_LEMMAS
from lexicon.wordform_gen import generate_noun_forms, generate_verb_forms
from lexicon.wordform_gen.rules_verbs import VERB_FORM_META

SUPPORTED_POS = ("s.", "a.", "v.", "pron.")
_PERSONAL_PRON = frozenset(lemma for lemma, _ in PERSONAL_PRONOUN_LEMMAS)
_INDECL_PRON = frozenset(INDECLINABLE_LEMMAS)


def ensure_verb_grammar_forms() -> dict:
    for code, name_krl, name_ru, sort_order in VERB_FORM_META:
        GrammarForm.objects.update_or_create(
            code=code,
            defaults={
                "name_krl": name_krl,
                "name_ru": name_ru,
                "category": GrammarForm.Category.VERB,
                "sort_order": sort_order,
            },
        )
    codes = [c for c, *_ in VERB_FORM_META]
    return {
        gf.code: gf
        for gf in GrammarForm.objects.filter(code__in=codes)
    }


class Command(BaseCommand):
    help = "Generate WordForm rows from Stem (nouns, adjectives, pronouns, verbs)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pos",
            default="s.",
            help="POS abbr: s., a., pron., or v. (default: s.)",
        )
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--limit", type=int, default=0)

    def handle(self, *args, **options):
        pos = options["pos"]
        dry_run = options["dry_run"]
        limit = options["limit"]

        if pos not in SUPPORTED_POS:
            self.stderr.write(
                f"Unsupported --pos={pos}. Implemented: {', '.join(SUPPORTED_POS)}"
            )
            return

        if pos == "v.":
            category = GrammarForm.Category.VERB
            gf_map = ensure_verb_grammar_forms()
        else:
            category = GrammarForm.Category.NOUN
            gf_map = {
                gf.code: gf
                for gf in GrammarForm.objects.filter(category=category)
            }

        if not gf_map:
            self.stderr.write(
                "No GrammarForm rows. Run: "
                "python manage.py loaddata lexicon/fixtures/grammar_forms.json"
            )
            return

        qs = (
            Word.objects.filter(pos__abbr=pos)
            .prefetch_related("stems")
            .order_by("id")
        )
        if limit:
            qs = list(qs[:limit])
        else:
            qs = list(qs)

        to_create = []
        words_ok = 0
        words_skip = 0

        for word in qs:
            if pos == "pron." and word.word_clean.lower() in _PERSONAL_PRON:
                words_skip += 1
                continue

            # Несклоняемые по глоссу Novak: только номинатив = лемма.
            if pos == "pron." and word.word_clean.lower() in _INDECL_PRON:
                gf = gf_map.get("nom_sg")
                if not gf:
                    words_skip += 1
                    continue
                orth_n = normalize_soft_sign(word.word.replace("|", ""))
                to_create.append(
                    WordForm(
                        word=word,
                        grammar_form=gf,
                        form=orth_n,
                        form_clean=Word.search_prepare(orth_n),
                    )
                )
                words_ok += 1
                continue

            stem_rows = sorted(word.stems.all(), key=lambda s: (s.number, s.alt))
            stems = {}
            for s in stem_rows:
                stems.setdefault(s.number, []).append(s.form)
            if not stems:
                words_skip += 1
                continue
            mark = next((s.special_mark for s in stem_rows if s.special_mark), "")

            if pos == "v.":
                forms = generate_verb_forms(
                    stems,
                    lemma=word.word.replace("|", ""),
                    special_mark=mark,
                )
            else:
                forms = generate_noun_forms(stems, special_mark=mark)

            if not forms:
                words_skip += 1
                continue

            words_ok += 1
            for code, orths in forms.items():
                gf = gf_map.get(code)
                if not gf:
                    continue
                for orth in orths:
                    orth_n = normalize_soft_sign(orth)
                    to_create.append(
                        WordForm(
                            word=word,
                            grammar_form=gf,
                            form=orth_n,
                            form_clean=Word.search_prepare(orth_n),
                        )
                    )

        self.stdout.write(
            f"words_ok={words_ok} skipped={words_skip} form_rows={len(to_create)}"
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("dry-run: DB not modified"))
            return

        with transaction.atomic():
            # Для pron.: не трогаем леммы Mestoimenia (их падежи тоже category=noun).
            qs_del = WordForm.objects.filter(
                grammar_form__category=category,
                word__pos__abbr=pos,
            )
            if pos == "pron.":
                qs_del = qs_del.exclude(word__word_clean__in=_PERSONAL_PRON)
            deleted, _ = qs_del.delete()
            WordForm.objects.bulk_create(to_create, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(
                f"replaced wordforms for {pos}: deleted={deleted}, created={len(to_create)}"
            )
        )
