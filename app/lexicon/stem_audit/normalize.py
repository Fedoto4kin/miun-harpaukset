"""Нормализация форм для сравнения (аудит / Dictorpus)."""

from __future__ import annotations

from lexicon.ortho import strip_soft_signs

_VOWELS = frozenset("aeiouyäöüáéíóúýå")


def form_key(text: str) -> str:
    """lower, ü→y, снять мягкий знак — ключ сравнения."""
    if not text:
        return ""
    return strip_soft_signs(text.lower().replace("ü", "y").replace("о", "o"))


def is_vowel(ch: str) -> bool:
    return bool(ch) and ch.lower() in _VOWELS


def suffix_body(sfx: str) -> str:
    s = (sfx or "").strip()
    return s[1:] if s.startswith("-") else s
