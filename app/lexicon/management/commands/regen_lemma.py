"""Точечная пересборка Stem + WordForm (noun/dim/poss/comp) для одной леммы."""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from lexicon.models import GrammarForm, Stem, Word, WordForm
from lexicon.ortho import normalize_soft_sign
from lexicon.stem_import import build_stems, parse_orig
from lexicon.stem_import.build_stems import resolve_special_mark
from lexicon.management.commands.generate_comparatives import (
    ensure_comp_grammar_forms,
)
from lexicon.management.commands.generate_diminutives import ensure_dim_grammar_forms
from lexicon.management.commands.generate_possessives import ensure_poss_grammar_forms
from lexicon.wordform_gen import (
    generate_comparative_forms,
    generate_diminutive_forms,
    generate_noun_forms,
    generate_possessive_forms,
)
from lexicon.wordform_gen.diminutives import dim_code


class Command(BaseCommand):
    help = "Rebuild stems + noun/dim/poss/comp wordforms for one lemma (after book fix)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--word",
            required=True,
            help="lemma word_clean or with |",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
        )
        parser.add_argument(
            "--skip-stems",
            action="store_true",
            help="Keep Stem rows; only regenerate WordForms from current stems",
        )

    def handle(self, *args, **options):
        only = (options["word"] or "").strip()
        bare = only.replace("|", "")
        word = (
            Word.objects.filter(pos__abbr__in=("s.", "a."))
            .filter(
                Q(word_clean__iexact=bare)
                | Q(word__iexact=only)
                | Q(word__iexact=bare)
            )
            .select_related("pos")
            .prefetch_related("stems")
            .first()
        )
        if not word:
            raise CommandError(f"Word not found (s./a.): {only}")

        pos = word.pos.abbr
        parsed = parse_orig(word.orig or "")
        lemma = word.word or parsed.lemma
        mark = resolve_special_mark(lemma, pos, parsed.special_mark)
        built = build_stems(lemma, parsed.code, pos, parsed.special_mark)

        self.stdout.write(
            f"lemma={lemma} code={parsed.code!r} mark={mark!r} "
            f"built_stem1={(built.get(1) or [None])[0]}"
        )

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("dry-run: DB not modified"))
            return

        with transaction.atomic():
            if not options["skip_stems"]:
                Stem.objects.filter(word=word).delete()
                to_stems = []
                for number, forms in built.items():
                    st = Stem.get_stem_type_for_number(pos, number)
                    if not st:
                        continue
                    for alt, form in enumerate(forms):
                        to_stems.append(
                            Stem(
                                word=word,
                                stem_type=st,
                                number=number,
                                alt=alt,
                                form=form,
                                special_mark=mark,
                            )
                        )
                Stem.objects.bulk_create(to_stems)
                self.stdout.write(f"stems={len(to_stems)}")

            stems: dict = {}
            for s in word.stems.all().order_by("number", "alt"):
                stems.setdefault(s.number, []).append(s.form)
            # refresh after recreate
            if not options["skip_stems"]:
                stems = {}
                for s in Stem.objects.filter(word=word).order_by("number", "alt"):
                    stems.setdefault(s.number, []).append(s.form)

            mark_db = next(
                (s.special_mark for s in Stem.objects.filter(word=word) if s.special_mark),
                mark,
            )

            gf_noun = {
                gf.code: gf
                for gf in GrammarForm.objects.filter(
                    category=GrammarForm.Category.NOUN
                )
            }
            WordForm.objects.filter(
                word=word, grammar_form__category=GrammarForm.Category.NOUN
            ).delete()
            noun_rows = []
            for code, orths in generate_noun_forms(stems, special_mark=mark_db).items():
                gf = gf_noun.get(code)
                if not gf:
                    continue
                for orth in orths:
                    orth_n = normalize_soft_sign(orth)
                    noun_rows.append(
                        WordForm(
                            word=word,
                            grammar_form=gf,
                            form=orth_n,
                            form_clean=Word.search_prepare(orth_n),
                        )
                    )
            WordForm.objects.bulk_create(noun_rows)

            dim_rows: list = []
            poss_rows: list = []
            comp_rows: list = []
            base = word.word.replace("|", "")
            # dim/poss — только для существительных
            if pos == "s.":
                dim_map = ensure_dim_grammar_forms()
                WordForm.objects.filter(
                    word=word,
                    grammar_form__category=GrammarForm.Category.DIMINUTIVE,
                ).delete()
                if not base.lower().endswith("ne") and mark_db != "pl":
                    for code, orths in generate_diminutive_forms(base).items():
                        gf = dim_map.get(dim_code(code))
                        if not gf:
                            continue
                        for orth in orths:
                            orth_n = normalize_soft_sign(orth)
                            dim_rows.append(
                                WordForm(
                                    word=word,
                                    grammar_form=gf,
                                    form=orth_n,
                                    form_clean=Word.search_prepare(orth_n),
                                )
                            )
                    WordForm.objects.bulk_create(dim_rows)

                poss_map = ensure_poss_grammar_forms()
                WordForm.objects.filter(
                    word=word,
                    grammar_form__category=GrammarForm.Category.POSSESSIVE,
                ).delete()
                for code, orths in generate_possessive_forms(
                    base, stems, include_dim=True
                ).items():
                    gf = poss_map.get(code)
                    if not gf:
                        continue
                    for orth in orths:
                        orth_n = normalize_soft_sign(orth)
                        poss_rows.append(
                            WordForm(
                                word=word,
                                grammar_form=gf,
                                form=orth_n,
                                form_clean=Word.search_prepare(orth_n),
                            )
                        )
                WordForm.objects.bulk_create(poss_rows)

            # comp — только прилагательные
            if pos == "a.":
                comp_map = ensure_comp_grammar_forms()
                WordForm.objects.filter(
                    word=word,
                    grammar_form__category=GrammarForm.Category.COMPARATIVE,
                ).delete()
                if mark_db != "pl":
                    for code, orths in generate_comparative_forms(
                        base, stems
                    ).items():
                        gf = comp_map.get(code)
                        if not gf:
                            continue
                        for orth in orths:
                            orth_n = normalize_soft_sign(orth)
                            surface_clean = Word.search_prepare(orth_n)
                            # как generate_comparatives: не дублировать отдельную статью
                            if (
                                surface_clean
                                and Word.objects.filter(
                                    Q(word_clean__iexact=surface_clean)
                                    | Q(word__iexact=surface_clean)
                                )
                                .exclude(pk=word.pk)
                                .exists()
                            ):
                                continue
                            comp_rows.append(
                                WordForm(
                                    word=word,
                                    grammar_form=gf,
                                    form=orth_n,
                                    form_clean=surface_clean,
                                )
                            )
                    WordForm.objects.bulk_create(comp_rows)

        gen = (
            WordForm.objects.filter(word=word, grammar_form__code="gen_sg")
            .values_list("form", flat=True)
            .first()
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"regen ok: noun={len(noun_rows)} dim={len(dim_rows)} "
                f"poss={len(poss_rows)} comp={len(comp_rows)} gen_sg={gen}"
            )
        )
