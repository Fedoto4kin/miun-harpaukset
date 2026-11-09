"""Разовая нормализация мягкого знака в Stem/WordForm → U+02BC."""

from django.core.management.base import BaseCommand
from django.db import transaction

from lexicon.models import Stem, Word, WordForm
from lexicon.ortho import SOFT_SIGN, normalize_soft_sign


class Command(BaseCommand):
    help = "Normalize soft-sign variants in Stem.form and WordForm.form to U+02BC"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        stem_n = 0
        wf_n = 0

        stems = list(Stem.objects.all().only("id", "form"))
        stem_updates = []
        for s in stems:
            new = normalize_soft_sign(s.form)
            if new != s.form:
                s.form = new
                stem_updates.append(s)
                stem_n += 1

        wfs = list(WordForm.objects.all().only("id", "form", "form_clean"))
        wf_updates = []
        for wf in wfs:
            new = normalize_soft_sign(wf.form)
            if new != wf.form or wf.form_clean != Word.search_prepare(new):
                wf.form = new
                wf.form_clean = Word.search_prepare(new)
                wf_updates.append(wf)
                wf_n += 1

        self.stdout.write(
            f"soft_canon={SOFT_SIGN!r} stem_to_fix={stem_n} wordform_to_fix={wf_n}"
        )
        if dry_run:
            self.stdout.write(self.style.WARNING("dry-run: DB not modified"))
            return

        with transaction.atomic():
            if stem_updates:
                Stem.objects.bulk_update(stem_updates, ["form"], batch_size=1000)
            if wf_updates:
                WordForm.objects.bulk_update(
                    wf_updates, ["form", "form_clean"], batch_size=1000
                )

        self.stdout.write(self.style.SUCCESS("normalized soft signs"))
