"""Притяжательные суффиксы -ni (1.yks.) и -š (2.yks.) для поиска.

В грамматике Новак (2020) парадигма суффиксов не описана: принадлежность
через miun/šiun + имя. В учебнике/фольклоре суффиксы живые
(Muamoš, izändäzeni, čikkozeni). Здесь — продуктивные формы для search-only
(category=possessive; не в таблице парадигмы).

Присоединение к гласной основе (как в примерах): stem + ni / š.
Уменьш.: …ze + ni / š → -zeni / -zeš.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

_VOWELS = frozenset("aeiouyäöüáéíóúýå")

# (code, name_krl, name_ru, sort_order)
POSS_FORM_META: Tuple[Tuple[str, str, str, int], ...] = (
    ("poss_1sg", "omistuš 1.yks. (-ni)", "притяж. 1л. ед. (-ni)", 2000),
    ("poss_2sg", "omistuš 2.yks. (-š)", "притяж. 2л. ед. (-š)", 2010),
    (
        "poss_dim_1sg",
        "pieniskö · omistuš 1.yks. (-zeni)",
        "уменьш. притяж. 1л. ед. (-zeni)",
        2020,
    ),
    (
        "poss_dim_2sg",
        "pieniskö · omistuš 2.yks. (-zeš)",
        "уменьш. притяж. 2л. ед. (-zeš)",
        2030,
    ),
)


def _is_vowel_final(form: str) -> bool:
    return bool(form) and form[-1].lower() in _VOWELS


def pick_vowel_stem(stem_forms: Dict[int, Sequence[str]], nom: str) -> Optional[str]:
    """
    Гласная основа для -ni/-š.
    Предпочтение: сильная ед. (2) → слабая ед. (1) → номинатив (0) → nom.
    """
    for number in (2, 1, 0):
        for form in stem_forms.get(number) or ():
            f = (form or "").strip()
            if _is_vowel_final(f):
                return f
    bare = (nom or "").strip()
    if _is_vowel_final(bare):
        return bare
    return None


def build_dim_ze_stem(nom: str) -> Optional[str]:
    """Основа …ze для -zeni/-zeš (тип hebone/alane)."""
    base = (nom or "").strip()
    if not base:
        return None
    low = base.lower()
    if low.endswith("ne"):
        # kirjane → kirjaze
        return base[:-2] + "ze"
    return base + "ze"


def generate_possessive_forms(
    nom: str,
    stem_forms: Optional[Dict[int, Sequence[str]]] = None,
    *,
    include_dim: bool = True,
) -> Dict[str, List[str]]:
    """
    Ключи: poss_1sg, poss_2sg, [poss_dim_1sg, poss_dim_2sg].

    Леммы на -ne (kirjane): притяжательные от основы …ze → kirjazeni / kirjazeš
    (отдельные dim-слоты не дублируем).
    """
    out: Dict[str, List[str]] = {}
    base = (nom or "").strip()
    if not base:
        return out

    if base.lower().endswith("ne"):
        ze = build_dim_ze_stem(base)
        if ze:
            out["poss_1sg"] = [ze + "ni"]
            out["poss_2sg"] = [ze + "š"]
        return out

    stem = pick_vowel_stem(stem_forms or {}, base)
    if stem:
        out["poss_1sg"] = [stem + "ni"]
        out["poss_2sg"] = [stem + "š"]

    if include_dim:
        ze = build_dim_ze_stem(base)
        if ze and _is_vowel_final(ze):
            out["poss_dim_1sg"] = [ze + "ni"]
            out["poss_dim_2sg"] = [ze + "š"]

    return out
