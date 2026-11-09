"""
Загрузка готовых парадигм местоимений (Mestoimenia.docx → data.py).

Не генерирует из Stem: только WordForm для известных лемм pos=pron.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from lexicon.models import WordForm
from lexicon.pronoun_import import (
    LEMMAS,
    build_wordform_rows,
    ensure_pronoun_grammar_forms,
)
from lexicon.pronoun_import.load import resolve_pronoun_words


class Command(BaseCommand):
    help = "Import ready-made pronoun paradigms into WordForm"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        gf_map = ensure_pronoun_grammar_forms()
        words, missing = resolve_pronoun_words()

        self.stdout.write(
            f"lemmas_in_table={len(LEMMAS)} matched={len(words)} missing={missing or '—'}"
        )

        rows = build_wordform_rows(words, gf_map)
        word_ids = [w.id for w in words.values()]

        self.stdout.write(f"form_rows={len(rows)}")

        if dry_run:
            self.stdout.write(self.style.WARNING("dry-run: DB not modified"))
            # sample
            for r in rows[:5]:
                self.stdout.write(
                    f"  {r.word.word_clean} {r.grammar_form.code}={r.form}"
                )
            return

        with transaction.atomic():
            deleted, _ = WordForm.objects.filter(word_id__in=word_ids).delete()
            WordForm.objects.bulk_create(rows, batch_size=500)

        self.stdout.write(
            self.style.SUCCESS(
                f"pronoun wordforms: deleted={deleted}, created={len(rows)}"
            )
        )
