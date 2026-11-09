"""Сборка WordForm для местоимений из встроенной таблицы."""

from __future__ import annotations

from typing import Dict, List, Tuple

from lexicon.models import GrammarForm, Word, WordForm
from lexicon.ortho import normalize_soft_sign

from .data import LEMMAS, iter_lemma_forms

# Аккузатив выделяется только у местоимений (Grammatika).
_ACC_FORMS = (
    (
        "acc_sg",
        "yksikön akkuzativa",
        "аккузатив ед.ч.",
        35,
    ),
    (
        "acc_pl",
        "monikon akkuzativa",
        "аккузатив мн.ч.",
        235,
    ),
)


def ensure_pronoun_grammar_forms() -> Dict[str, GrammarForm]:
    """Гарантирует acc_sg/acc_pl; возвращает map code→GrammarForm для нужных кодов."""
    for code, name_krl, name_ru, sort_order in _ACC_FORMS:
        GrammarForm.objects.update_or_create(
            code=code,
            defaults={
                "name_krl": name_krl,
                "name_ru": name_ru,
                "category": GrammarForm.Category.PRON,
                "sort_order": sort_order,
            },
        )

    needed = {code for _, _, code, _ in iter_lemma_forms()}
    gf_map = {
        gf.code: gf
        for gf in GrammarForm.objects.filter(code__in=needed)
    }
    missing = needed - set(gf_map)
    if missing:
        raise RuntimeError(
            "Missing GrammarForm codes: "
            f"{sorted(missing)}. Load lexicon/fixtures/grammar_forms.json"
        )
    return gf_map


def resolve_pronoun_words() -> Tuple[Dict[str, Word], List[str]]:
    """lemma → Word (pos=pron.); список лемм без записи в словаре."""
    wanted = {lemma for lemma, _ in LEMMAS}
    found: Dict[str, Word] = {}
    qs = Word.objects.filter(pos__abbr="pron.", word_clean__in=wanted)
    for w in qs:
        # при дубликатах берём меньший id
        prev = found.get(w.word_clean)
        if prev is None or w.id < prev.id:
            found[w.word_clean] = w
    missing = sorted(wanted - set(found))
    return found, missing


def build_wordform_rows(
    words: Dict[str, Word],
    gf_map: Dict[str, GrammarForm],
) -> List[WordForm]:
    rows: List[WordForm] = []
    for lemma, _number, code, form in iter_lemma_forms():
        word = words.get(lemma)
        if not word:
            continue
        gf = gf_map[code]
        form_n = normalize_soft_sign(form)
        rows.append(
            WordForm(
                word=word,
                grammar_form=gf,
                form=form_n,
                form_clean=Word.search_prepare(form_n),
            )
        )
    return rows
