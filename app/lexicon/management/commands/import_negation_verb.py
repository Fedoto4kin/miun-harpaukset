"""
Загрузка готовой парадигмы отрицательного глагола ei.

Не генерирует из Stem: только WordForm для леммы pos=v. negat.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from lexicon.models import WordForm
from lexicon.negation_verb_import import (
    LEMMA,
    PARADIGM,
    build_wordform_rows,
    ensure_grammar_forms,
    resolve_ei_word,
)


class Command(BaseCommand):
    help = "Import ready-made negation verb (ei) paradigm into WordForm"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        gf_map = ensure_grammar_forms()
        word, err = resolve_ei_word()
        if err:
            self.stderr.write(self.style.ERROR(err))
            return

        rows = build_wordform_rows(word, gf_map)
        self.stdout.write(
            f"lemma={LEMMA} word_id={word.id} form_rows={len(rows)}"
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("dry-run: DB not modified"))
            for r in rows:
                self.stdout.write(f"  {r.grammar_form.code}={r.form}")
            return

        with transaction.atomic():
            deleted, _ = WordForm.objects.filter(word_id=word.id).delete()
            WordForm.objects.bulk_create(rows, batch_size=100)

        self.stdout.write(
            self.style.SUCCESS(
                f"ei wordforms: deleted={deleted}, created={len(rows)} "
                f"({', '.join(PARADIGM.values())})"
            )
        )
