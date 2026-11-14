"""Сравнительная степень прилагательных на -mbi (Grammatika Novak / учебник).

Не runtime: оффлайн WordForm на базовой лемме a., category=comparative,
search-only (не в таблице парадигмы).

Правило: слабая гласная основа + mbi; конечные a/ä → e
(šoma → šomembi; pieni/stem piene → pienembi; armaš/stem armahe → armahembi).

Супплетивы (hyvä → parembi) и отдельные словарные статьи (*mbi) — skip
на стороне generate_comparatives.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

_VOWELS = frozenset("aeiouyäöüáéíóúýå")

# Супплетивные базы: продуктивный -mbi не строим (есть отдельная лемма).
SUPPLETIVE_SKIP = frozenset({"hyvä"})

COMP_FORM_META: Tuple[Tuple[str, str, str, int], ...] = (
    (
        "comp",
        "komparativa",
        "сравнительная степень",
        2100,
    ),
)


def _is_vowel_final(form: str) -> bool:
    return bool(form) and form[-1].lower() in _VOWELS


def pick_comparative_stem(
    stem_forms: Optional[Dict[int, Sequence[str]]],
    nom: str,
) -> Optional[str]:
    """Слабая гласная основа: stem1 → stem2 → stem0 → nom."""
    for number in (1, 2, 0):
        for form in (stem_forms or {}).get(number) or ():
            f = (form or "").strip()
            if f and _is_vowel_final(f):
                return f
    bare = (nom or "").strip()
    if bare and _is_vowel_final(bare):
        return bare
    return None


def _final_ci_to_e(stem: str) -> str:
    """Исход на Ci (не дифтонг Vi): перед -mbi обычно Ce (pieni→piene)."""
    low = stem.lower()
    if len(stem) >= 2 and low.endswith("i") and low[-2] not in _VOWELS:
        return stem[:-1] + "e"
    return stem


def apply_a_ae_to_e(stem: str) -> str:
    """Конечные a/ä основы → e перед -mbi (Grammatika)."""
    if not stem:
        return stem
    last = stem[-1]
    if last == "a":
        return stem[:-1] + "e"
    if last == "ä":
        return stem[:-1] + "e"
    if last == "A":
        return stem[:-1] + "E"
    if last == "Ä":
        return stem[:-1] + "E"
    return stem


def build_comparative_nom(
    nom: str,
    stem_forms: Optional[Dict[int, Sequence[str]]] = None,
) -> Optional[str]:
    """
    Номинатив сравнительной степени или None, если неприменимо.
    Не проверяет sibling/супплетивы — это в management command.
    """
    base = (nom or "").strip()
    if not base:
        return None
    low = base.lower()
    if low in SUPPLETIVE_SKIP:
        return None
    if low.endswith("mbi"):
        return None

    stem = pick_comparative_stem(stem_forms, base)
    if not stem:
        return None
    stem = _final_ci_to_e(stem)
    stem = apply_a_ae_to_e(stem)
    if not _is_vowel_final(stem):
        return None
    return stem + "mbi"


def generate_comparative_forms(
    nom: str,
    stem_forms: Optional[Dict[int, Sequence[str]]] = None,
) -> Dict[str, List[str]]:
    """Ключ: comp → [орфография]."""
    form = build_comparative_nom(nom, stem_forms)
    if not form:
        return {}
    return {"comp": [form]}
