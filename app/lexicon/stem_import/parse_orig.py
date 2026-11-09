"""Парсинг HTML Word.orig → структурированные поля шаблона основ."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

_RE_BOLD = re.compile(r"<b>\s*(.*?)\s*</b>", re.IGNORECASE | re.DOTALL)
_RE_CODE = re.compile(r"<code>\s*(.*?)\s*</code>", re.IGNORECASE | re.DOTALL)
_RE_ITALIC = re.compile(r"<i>\s*(.*?)\s*</i>", re.IGNORECASE | re.DOTALL)

# Пометы в <i>: "s. pl.", "v. def.", "pron. sing." …
_RE_MARK_PL = re.compile(r"\bpl\b", re.IGNORECASE)
_RE_MARK_SING = re.compile(r"\bsing\b", re.IGNORECASE)
_RE_MARK_VDEF = re.compile(r"\bv\.\s*def\b", re.IGNORECASE)

# POS abbr из <i>, допускаем пробелы: "s.", "v. def.", "kield. v."
_POS_PREFIXES = (
    "v. def.",
    "v. negat.",
    "kield. v.",
    "pron.",
    "partic.",
    "interj.",
    "postp.",
    "prep.",
    "conj.",
    "adv.",
    "num.",
    "a.",
    "s.",
    "v.",
)


@dataclass(frozen=True)
class ParsedOrig:
    """Результат разбора одной словарной статьи."""

    lemma: str  # как в <b>, с возможным |
    code: Optional[str]  # содержимое <code>, без тегов; None если нет
    pos_abbr: Optional[str]  # нормализованный abbr: s. / a. / v. / …
    special_mark: str  # "" | "pl" | "sing" | "v_def"
    raw_italic: Optional[str] = None


def parse_orig(orig: str) -> ParsedOrig:
    """
    Извлекает лемму, шаблон основ и пометы из HTML orig.

    Не бросает исключений на битый HTML — возвращает пустые поля.
    """
    if not orig:
        return ParsedOrig(lemma="", code=None, pos_abbr=None, special_mark="")

    lemma = _first_group(_RE_BOLD, orig) or ""
    code = _first_group(_RE_CODE, orig)
    if code is not None:
        code = _normalize_ws(code)

    italic = _first_group(_RE_ITALIC, orig)
    italic_norm = _normalize_ws(italic) if italic else None

    pos_abbr = _extract_pos(italic_norm) if italic_norm else None
    special_mark = _extract_mark(italic_norm) if italic_norm else ""

    return ParsedOrig(
        lemma=lemma.strip(),
        code=code,
        pos_abbr=pos_abbr,
        special_mark=special_mark,
        raw_italic=italic_norm,
    )


def _first_group(pattern: re.Pattern, text: str) -> Optional[str]:
    m = pattern.search(text)
    if not m:
        return None
    return m.group(1)


def _normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _extract_pos(italic: str) -> Optional[str]:
    lowered = italic.lower().strip()
    for prefix in _POS_PREFIXES:
        if lowered.startswith(prefix):
            # нормализуем известные варианты
            if prefix == "kield. v.":
                return "v. negat."
            if prefix == "v. def.":
                return "v."
            return prefix
    # fallback: первое слово-токен с точкой
    m = re.match(r"([a-z]+\.(?:\s*[a-z]+\.)?)", lowered)
    return m.group(1).strip() if m else None


def _extract_mark(italic: str) -> str:
    if _RE_MARK_VDEF.search(italic):
        return "v_def"
    if _RE_MARK_PL.search(italic):
        return "pl"
    if _RE_MARK_SING.search(italic):
        return "sing"
    return ""
