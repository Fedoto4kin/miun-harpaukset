"""
Продуктивные уменьшительные s. на -ne → WordForm (category=diminutive).

Не трогает каноническую парадигму. Skip: уже *ne-леммы и словарные sibling *ne.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from lexicon.models import GrammarForm, Word, WordForm
from lexicon.ortho import normalize_soft_sign
from lexicon.wordform_gen.diminutives import (
    DIM_FORM_META,
    dim_code,
    generate_diminutive_forms,
)


def ensure_dim_grammar_forms() -> dict:
    for code, name_krl, name_ru, sort_order in DIM_FORM_META:
        GrammarForm.objects.update_or_create(
            code=code,
            defaults={
                "name_krl": name_krl,
                "name_ru": name_ru,
                "category": GrammarForm.Category.DIMINUTIVE,
                "sort_order": sort_order,
            },
        )
    codes = [c for c, *_ in DIM_FORM_META]
    return {
        gf.code: gf
        for gf in GrammarForm.objects.filter(code__in=codes)
    }


def _has_ne_sibling(word: Word, base_clean: str) -> bool:
    """Есть отдельная словарная статья base+ne (kirja→kirjane)."""
    cand = base_clean.lower() + "ne"
    return (
        Word.objects.filter(pos__abbr="s.")
        .filter(Q(word_clean__iexact=cand) | Q(word__iexact=cand))
        .exclude(pk=word.pk)
        .exists()
    )


class Command(BaseCommand):
    help = "Generate productive -ne diminutive WordForms for nouns (s.)"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument(
            "--word",
            default="",
            help="Только одна лемма (word_clean или с |), для отладки",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]
        only = (options["word"] or "").strip()

        gf_map = ensure_dim_grammar_forms()
        if not gf_map:
            self.stderr.write("Failed to ensure diminutive GrammarForm rows")
            return

        qs = (
            Word.objects.filter(pos__abbr="s.")
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
        if limit:
            qs = list(qs[:limit])
        else:
            qs = list(qs)

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
            if base_clean.endswith("ne"):
                words_skip += 1
                continue
            if _has_ne_sibling(word, base_clean):
                words_skip += 1
                continue

            forms = generate_diminutive_forms(nom)
            if not forms:
                words_skip += 1
                continue

            words_ok += 1
            for code, orths in forms.items():
                gf = gf_map.get(dim_code(code))
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
                grammar_form__category=GrammarForm.Category.DIMINUTIVE,
                word__pos__abbr="s.",
            ).delete()
            WordForm.objects.bulk_create(to_create, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(
                f"diminutives: deleted={deleted}, created={len(to_create)}"
            )
        )
