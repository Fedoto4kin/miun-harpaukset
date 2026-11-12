"""Сборка WordForm для отрицательного глагола ei."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from lexicon.models import GrammarForm, Word, WordForm
from lexicon.ortho import normalize_soft_sign

from .data import LEMMA, POS_ABBR, form_codes, iter_forms


def resolve_ei_word() -> Tuple[Optional[Word], Optional[str]]:
    """Word с pos=v. negat. и word_clean=ei; иначе (None, причина)."""
    qs = Word.objects.filter(pos__abbr=POS_ABBR, word_clean=LEMMA).order_by("id")
    word = qs.first()
    if word is None:
        return None, f"no Word word_clean={LEMMA!r} pos={POS_ABBR!r}"
    return word, None


def ensure_grammar_forms() -> Dict[str, GrammarForm]:
    needed = set(form_codes())
    gf_map = {
        gf.code: gf for gf in GrammarForm.objects.filter(code__in=needed)
    }
    missing = needed - set(gf_map)
    if missing:
        raise RuntimeError(
            "Missing GrammarForm codes: "
            f"{sorted(missing)}. Load lexicon fixtures / generate_wordforms --pos=v."
        )
    return gf_map


def build_wordform_rows(
    word: Word,
    gf_map: Dict[str, GrammarForm],
) -> List[WordForm]:
    rows: List[WordForm] = []
    for code, form in iter_forms():
        form_n = normalize_soft_sign(form)
        rows.append(
            WordForm(
                word=word,
                grammar_form=gf_map[code],
                form=form_n,
                form_clean=Word.search_prepare(form_n),
            )
        )
    return rows
