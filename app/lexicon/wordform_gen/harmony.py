"""Гармония гласных по Grammatika: a/o/u в основе → задний ряд."""

from __future__ import annotations

_BACK_VOWELS = set("aouAOU")


def is_back_harmony(stem: str) -> bool:
    """True, если в основе есть a, o или u → берём левый вариант окончания."""
    return any(ch in _BACK_VOWELS for ch in stem)


def pick(stem: str, back: str, front: str) -> str:
    return back if is_back_harmony(stem) else front
