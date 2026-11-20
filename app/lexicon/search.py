"""Нормализация строки для поиска по словарю."""

from __future__ import annotations

from lexicon.ortho import strip_soft_signs

# Карельский алфавит (источник истины для поиска / slugify).
KRL_ABC = "ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ"
_ALLOWED = frozenset(KRL_ABC.lower() + " |")


def search_prepare(string: str) -> str:
    """lower, ü→y, снять мягкий знак, оставить KRL_ABC + пробел + ``|``."""
    if not string:
        return ""
    normalized = strip_soft_signs(string.lower().replace("ü", "y"))
    return "".join(ch for ch in normalized if ch in _ALLOWED)


def normalize_definition_search(string: str) -> str:
    """lower + ё→е для reverse-поиска по переводам (RU)."""
    if not string:
        return ""
    return string.lower().replace("ё", "е")
