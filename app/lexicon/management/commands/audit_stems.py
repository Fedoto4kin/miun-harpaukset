"""Аудит основ: слой 1 (структура) и слой 2 (Dictorpus d47)."""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import Prefetch

from lexicon.models import Word, WordForm
from lexicon.stem_audit.dictorpus import dump_jsonl, enrich_with_dictorpus
from lexicon.stem_audit.report import write_book_arbitration_md
from lexicon.stem_audit.structural import AUDITABLE_POS, audit_structural


def _parse_pos_list(raw: str) -> list[str]:
    parts = [p.strip() for p in (raw or "").split(",") if p.strip()]
    return parts or ["s."]


def _word_row(word) -> dict:
    forms = {wf.grammar_form.code: wf.form for wf in word._audit_forms}
    stems: dict = {}
    for s in word.stems.all():
        stems.setdefault(s.number, []).append(s.form)
    return {
        "word_id": word.id,
        "lemma": word.word,
        "lemma_clean": word.word_clean,
        "pos": word.pos.abbr,
        "code": None,
        "stem1": (stems.get(1) or [None])[0],
        "stem2": (stems.get(2) or [None])[0],
        "stem3": (stems.get(3) or [None])[0],
        "gen_sg": forms.get("gen_sg"),
        "part_sg": forms.get("part_sg"),
        "ill_sg": forms.get("ill_sg"),
        "iness_sg": forms.get("iness_sg"),
        "ades_sg": forms.get("ades_sg"),
        "reasons": [],
        "dictorpus_url": (
            "http://dictorpus.krc.karelia.ru/ru/dict/wordform"
            f"?search_dialect=47&search_lang=4"
            f"&search_lemma={word.word_clean}&limit_num=50"
        ),
    }


class Command(BaseCommand):
    help = "Audit stems (structural + optional Dictorpus dialect=47)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--layer",
            choices=("1", "2", "all"),
            default="1",
            help="1=structural; 2=dictorpus on suspects (or --full-pos); all=1+2",
        )
        parser.add_argument(
            "--pos",
            default="s.",
            help="POS abbr or comma-list: s.,a.,pron.,v. (default s.)",
        )
        parser.add_argument(
            "--full-pos",
            action="store_true",
            help="Layer 2 over all selected POS lemmas, not only structural suspects",
        )
        parser.add_argument("--out", default="", help="JSONL output path")
        parser.add_argument(
            "--book-md",
            default="",
            help="Markdown checklist for book arbitration (layer 3)",
        )
        parser.add_argument(
            "--cache-dir",
            default="/tmp/dictorpus_cache",
            help="HTML cache for Dictorpus fetches",
        )
        parser.add_argument("--limit", type=int, default=0, help="0=all")
        parser.add_argument(
            "--force-fetch",
            action="store_true",
            help="Ignore Dictorpus cache",
        )

    def handle(self, *args, **options):
        pos_list = _parse_pos_list(options["pos"])
        bad = [p for p in pos_list if p not in AUDITABLE_POS]
        if bad:
            self.stderr.write(
                f"Unsupported POS: {bad}. Allowed: {', '.join(sorted(AUDITABLE_POS))}"
            )
            return

        layer = options["layer"]
        limit = options["limit"]
        out_path = (options["out"] or "").strip()
        book_md = (options["book_md"] or "").strip()

        form_qs = WordForm.objects.filter(
            grammar_form__code__in=[
                "gen_sg",
                "part_sg",
                "ill_sg",
                "iness_sg",
                "ades_sg",
            ]
        ).select_related("grammar_form")

        qs = (
            Word.objects.filter(pos__abbr__in=pos_list)
            .select_related("pos")
            .prefetch_related("stems", Prefetch("wordform_set", queryset=form_qs))
            .order_by("pos__abbr", "id")
        )
        words = list(qs[:limit] if limit else qs)
        for w in words:
            w._audit_forms = list(w.wordform_set.all())

        structural = audit_structural(words)
        self.stdout.write(
            f"layer1: pos={pos_list} words={len(words)} suspects={len(structural)}"
        )
        by_reason: dict = {}
        by_pos: dict = {}
        for row in structural:
            by_pos[row.get("pos") or "?"] = by_pos.get(row.get("pos") or "?", 0) + 1
            for r in row["reasons"]:
                by_reason[r] = by_reason.get(r, 0) + 1
        for p, n in sorted(by_pos.items()):
            self.stdout.write(f"  pos {p}: {n}")
        for r, n in sorted(by_reason.items()):
            self.stdout.write(f"  {r}: {n}")

        if layer == "1":
            rows = structural
        else:
            if options["full_pos"]:
                rows = [_word_row(w) for w in words]
            else:
                rows = list(structural)
            self.stdout.write(
                f"layer2: Dictorpus for {len(rows)} lemmas "
                f"(cache={options['cache_dir']})"
            )
            rows = enrich_with_dictorpus(
                rows,
                cache_dir=Path(options["cache_dir"]),
                force_fetch=options["force_fetch"],
            )
            need_book = sum(1 for r in rows if r.get("needs_book"))
            self.stdout.write(f"layer2: needs_book={need_book}")

        if out_path:
            n = dump_jsonl(Path(out_path), rows)
            self.stdout.write(self.style.SUCCESS(f"wrote {n} rows → {out_path}"))

        if book_md:
            n = write_book_arbitration_md(Path(book_md), rows)
            self.stdout.write(self.style.SUCCESS(f"book checklist {n} → {book_md}"))
