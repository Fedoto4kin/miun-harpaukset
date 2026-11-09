"""
Разово заполняет lexicon_stem из Word.orig.

Парсер живёт в lexicon.stem_import (не runtime).
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from lexicon.models import Stem, Word
from lexicon.stem_import import build_stems, parse_orig
from lexicon.stem_import.build_stems import resolve_special_mark

_IMPORTABLE_POS = frozenset({"s.", "a.", "v.", "pron."})


class Command(BaseCommand):
    help = "Parse Word.orig templates into Stem rows (one-shot import)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report counts without writing to DB",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Process at most N words (0 = all)",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]

        qs = (
            Word.objects.select_related("pos")
            .filter(pos__abbr__in=_IMPORTABLE_POS)
            .order_by("id")
        )
        if limit:
            qs = qs[:limit]

        parsed_ok = 0
        with_stems = 0
        skipped_no_code = 0
        errors = 0
        to_create = []

        for word in qs.iterator():
            try:
                parsed = parse_orig(word.orig or "")
                pos = word.pos.abbr
                if pos not in _IMPORTABLE_POS:
                    continue

                lemma = word.word or parsed.lemma
                mark = resolve_special_mark(lemma, pos, parsed.special_mark)
                stems = build_stems(lemma, parsed.code, pos, parsed.special_mark)
                parsed_ok += 1

                if parsed.code is None:
                    skipped_no_code += 1

                if len(stems) <= 1 and parsed.code is None:
                    continue

                with_stems += 1
                stem_type_fn = Stem.get_stem_type_for_number
                for number, forms in stems.items():
                    stem_type = stem_type_fn(pos, number)
                    if not stem_type:
                        continue
                    for alt, form in enumerate(forms):
                        to_create.append(
                            Stem(
                                word=word,
                                stem_type=stem_type,
                                number=number,
                                alt=alt,
                                form=form,
                                special_mark=mark,
                            )
                        )
            except Exception as exc:  # noqa: BLE001
                errors += 1
                self.stderr.write(f"id={word.id} {word.word}: {exc}")

        self.stdout.write(
            f"words={parsed_ok} with_template_stems={with_stems} "
            f"no_code={skipped_no_code} errors={errors} "
            f"stem_rows={len(to_create)}"
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("dry-run: DB not modified"))
            return

        with transaction.atomic():
            deleted, _ = Stem.objects.all().delete()
            Stem.objects.bulk_create(to_create, batch_size=500)

        self.stdout.write(
            self.style.SUCCESS(f"replaced stems: deleted={deleted}, created={len(to_create)}")
        )
