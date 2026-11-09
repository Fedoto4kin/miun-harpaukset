"""Канон мягкого знака и нормализация для поиска/хранения."""

from __future__ import annotations

# Канон в Stem / WordForm / генераторах (modifier letter apostrophe).
SOFT_SIGN = "\u02bc"  # ʼ

# Встречающиеся варианты (учебник, Dictorpus, orig).
_SOFT_VARIANTS = (
    "\u02bc",  # ʼ modifier letter apostrophe
    "\u2019",  # ’ right single quotation mark
    "\u02b9",  # ʹ modifier letter prime
    "'",  # ASCII apostrophe
)

_SOFT_TO_CANON = {ch: SOFT_SIGN for ch in _SOFT_VARIANTS}
_SOFT_STRIP = {ch: "" for ch in _SOFT_VARIANTS}


def normalize_soft_sign(text: str) -> str:
    """Все варианты мягкого знака → U+02BC (для хранения форм)."""
    if not text:
        return text
    return "".join(_SOFT_TO_CANON.get(ch, ch) for ch in text)


def strip_soft_signs(text: str) -> str:
    """Снять все варианты мягкого знака (поиск / word_clean)."""
    if not text:
        return text
    return "".join(_SOFT_STRIP.get(ch, ch) for ch in text)
