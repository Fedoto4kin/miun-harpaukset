"""Импорт готовых парадигм местоимений (не runtime API)."""

from .data import INDECLINABLE_LEMMAS, LEMMAS, PARADIGM, iter_lemma_forms
from .load import build_wordform_rows, ensure_pronoun_grammar_forms

__all__ = [
    "INDECLINABLE_LEMMAS",
    "LEMMAS",
    "PARADIGM",
    "iter_lemma_forms",
    "build_wordform_rows",
    "ensure_pronoun_grammar_forms",
]
