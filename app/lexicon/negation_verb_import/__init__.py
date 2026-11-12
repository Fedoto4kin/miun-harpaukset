"""Импорт готовой парадигмы отрицательного глагола ei (не runtime API)."""

from .data import LEMMA, PARADIGM, POS_ABBR, form_codes, iter_forms
from .load import build_wordform_rows, ensure_grammar_forms, resolve_ei_word

__all__ = [
    "LEMMA",
    "PARADIGM",
    "POS_ABBR",
    "form_codes",
    "iter_forms",
    "build_wordform_rows",
    "ensure_grammar_forms",
    "resolve_ei_word",
]
