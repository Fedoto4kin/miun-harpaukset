"""
Сравнительная степень a. на -mbi → WordForm (category=comparative), search-only.

Не трогает каноническую парадигму / dim / poss.
Skip: special_mark=pl; супплетивы (hyvä); леммы на -mbi;
отдельная словарная статья с той же поверхностью (parembi, vanhembi).
"""

from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from lexicon.models import GrammarForm, Word, WordForm
from lexicon.ortho import normalize_soft_sign
from lexicon.wordform_gen.comparatives import (
    COMP_FORM_META,
    generate_comparative_forms,
)


def ensure_comp_grammar_forms() -> dict:
    for code, name_krl, name_ru, sort_order in COMP_FORM_META:
        GrammarForm.objects.update_or_create(
            code=code,
            defaults={
                "name_krl": name_krl,
                "name_ru": name_ru,
                "category": GrammarForm.Category.COMPARATIVE,
                "sort_order": sort_order,
            },
        )
    codes = [c for c, *_ in COMP_FORM_META]
    return {
        gf.code: gf
        for gf in GrammarForm.objects.filter(code__in=codes)
    }


def _has_surface_sibling(word: Word, surface_clean: str) -> bool:
    """Уже есть статья с word_clean == сгенерированная форма."""
    return (
        Word.objects.filter(
            Q(word_clean__iexact=surface_clean) | Q(word__iexact=surface_clean)
        )
        .exclude(pk=word.pk)
        .exists()
    )


def _stem_map(word: Word) -> dict:
    by_num = defaultdict(list)
    for s in word.stems.all():
        if s.form:
            by_num[s.number].append(s.form)
    return dict(by_num)


class Command(BaseCommand):
    help = "Generate comparative -mbi WordForms for adjectives (a.), search-only"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument(
            "--word",
            default="",
            help="Только одна лемма (word_clean или с |)",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]
        only = (options["word"] or "").strip()

        gf_map = ensure_comp_grammar_forms()
        if not gf_map:
            self.stderr.write("Failed to ensure comparative GrammarForm rows")
            return

        qs = (
            Word.objects.filter(pos__abbr="a.")
            .prefetch_related("stems")
            .order_by("id")
        )
        if only:
            bare = only.replace("|", "")
            qs = qs.filter(
                Q(word_clean__iexact=bare)
                | Q(word__iexact=only)
                | Q(word__iexact=bare)
            )
        qs = list(qs[:limit] if limit else qs)

        to_create = []
        words_ok = 0
        words_skip = 0

        for word in qs:
            stem0 = next(
                (s.form for s in word.stems.all() if s.number == 0 and s.alt == 0),
                None,
            )
            nom = stem0 or word.word.replace("|", "")
            base_clean = Word.search_prepare(nom)
            if not base_clean:
                words_skip += 1
                continue

            mark = next(
                (s.special_mark for s in word.stems.all() if s.special_mark),
                "",
            )
            if mark == "pl":
                words_skip += 1
                continue

            forms = generate_comparative_forms(nom, _stem_map(word))
            if not forms:
                words_skip += 1
                continue

            # sibling: vanha→vanhembi, если vanhembi уже статья
            surface = forms["comp"][0]
            surface_clean = Word.search_prepare(normalize_soft_sign(surface))
            if surface_clean and _has_surface_sibling(word, surface_clean):
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
            deleted, _ = WordForm.objects.filter(
                grammar_form__category=GrammarForm.Category.COMPARATIVE,
                word__pos__abbr="a.",
            ).delete()
            WordForm.objects.bulk_create(to_create, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(
                f"comparatives: deleted={deleted}, created={len(to_create)}"
            )
        )
