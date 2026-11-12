"""Сборка полных основ из леммы и шаблона <code>."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Sequence, Tuple

from lexicon.ortho import normalize_soft_sign, strip_soft_signs

# Чередование слабая : сильная (в данных встречается и ;)
_ALT_SPLIT = re.compile(r"\s*[:;]\s*")
# Альтернативные варианты основы (Grammatika: 4/5 могут иметь 2 варианта)
_SLASH_SPLIT = re.compile(r"\s*/\s*")

# Слот = список альтернатив; альтернатива = (weak, strong|None)
SlotAlts = List[Tuple[str, Optional[str]]]
StemMap = Dict[int, List[str]]

# Глоссарий Novak: правки поверх шаблона <code> / помет.
# lemma_clean → {номер: [формы]} (полная замена слотов).
_BOOK_STEM_OVERRIDES: Dict[str, Dict[int, List[str]]] = {
    "ken": {1: ["kene"], 2: ["kene"]},
    "niken": {1: ["nikene"], 2: ["nikene"]},
    # še (šen, šidä); шаблон -i,-dä даёт ši/šdä
    "še": {1: ["še"], 2: ["še"], 3: ["šidä"]},
    # moni (monen, monie); шаблон -da даёт monda
    "moni": {3: ["monie"]},
    # kumbane (kumbezen, kummasʼtʼa); шаблон -baze → kumbaze
    "kumbane": {1: ["kumbeze"], 2: ["kumbeze"]},
    # nua/nuo (noin, noida)
    "nuo": {4: ["noi"], 5: ["noi"]},
    "nua": {4: ["noi"], 5: ["noi"]},
    # molemmat (molemmin, molembie) pl. tantum
    "molemmat": {1: ["molemmi"], 2: ["molembi"], 3: ["molembie"], 4: ["molemmi"], 5: ["molembi"]},
    # rebo: в <code> сокращение -v : -bo → иначе revn вместо revon (Dictorpus/учебник)
    "rebo": {1: ["revo"]},
}

# Полная пересборка по глоссу (игнор ошибочной пометы pl. в orig и т.п.).
# lemma_clean → (special_mark, code) как у именного шаблона.
_BOOK_TEMPLATE_OVERRIDES: Dict[str, tuple] = {
    # глосс: mi (min, midä); в orig ошибочно «pron. pl.»
    "mi": ("sing", "-, -dä"),
    # глосс: nimi II (nimin, nimidä); в orig ошибочно «pron. pl.»
    "nimi": ("sing", "-, -dä"),
    # molemmat — pl. tantum (в orig кривая вложенная помета)
    "molemmat": ("pl", "-mi : -bi"),
}


def stem_base(lemma: str) -> str:
    """База для суффиксов: часть до |, иначе целая лемма без |."""
    if "|" in lemma:
        return normalize_soft_sign(lemma.split("|", 1)[0])
    return normalize_soft_sign(lemma.replace("|", ""))


def lemma_clean(lemma: str) -> str:
    return strip_soft_signs(lemma.replace("|", ""))


def apply_suffix(base: str, suffix: str) -> str:
    """
    Применяет словарный суффикс к базе.
    '-' или пусто → только база; '-da' → base+'da'.
    """
    s = suffix.strip()
    if s in ("", "-"):
        return normalize_soft_sign(base)
    if s.startswith("-"):
        s = s[1:]
    return normalize_soft_sign(base + s)


def parse_template_slots(code: str) -> List[SlotAlts]:
    """
    Делит шаблон на слоты по запятым.
    Внутри слота `/` — альтернативы; внутри альтернативы `:`/`;` — слабая:сильная.
    Пример: `-zi / -zilöi` → [[('-zi', None), ('-zilöi', None)]]
    """
    if not code or not code.strip():
        return []

    slots: List[SlotAlts] = []
    for raw in code.split(","):
        part = raw.strip()
        if not part:
            continue
        alts: SlotAlts = []
        for alt_raw in _SLASH_SPLIT.split(part):
            alt = alt_raw.strip()
            if not alt:
                continue
            pieces = _ALT_SPLIT.split(alt)
            if len(pieces) == 1:
                alts.append((pieces[0].strip(), None))
            else:
                alts.append((pieces[0].strip(), pieces[1].strip()))
        if alts:
            slots.append(alts)
    return slots


def build_stems(
    lemma: str,
    code: Optional[str],
    pos_abbr: Optional[str],
    special_mark: str = "",
) -> StemMap:
    """
    Возвращает {номер_основы: [форма_alt0, форма_alt1, ...]}.

    Основа 0 всегда = лемма без |.
    Поддерживаются pos: s., a., v., pron. (именная схема).
    """
    clean = lemma_clean(lemma)
    if not clean:
        return {}

    # Основа 0 хранит канонический мягкий знак, если он был в лемме.
    stem0 = normalize_soft_sign(lemma.replace("|", ""))
    stems: StemMap = {0: [stem0]}

    book_tpl = _BOOK_TEMPLATE_OVERRIDES.get(clean.lower())
    if book_tpl and pos_abbr in ("s.", "a.", "pron."):
        special_mark, code = book_tpl

    if not code or not pos_abbr:
        return stems

    base = stem_base(lemma)
    slots = parse_template_slots(code)
    if not slots:
        return _apply_book_overrides(clean, stems)

    if pos_abbr in ("s.", "a.", "pron."):
        stems.update(_build_nominal(base, slots, special_mark))
    elif pos_abbr == "v.":
        stems.update(_build_verb(base, slots, special_mark))

    return _apply_book_overrides(clean, stems)


def _apply_book_overrides(lemma_key: str, stems: StemMap) -> StemMap:
    overrides = _BOOK_STEM_OVERRIDES.get(lemma_key.lower())
    if not overrides:
        return stems
    for number, forms in overrides.items():
        stems[number] = list(forms)
    return stems


def resolve_special_mark(
    lemma: str, pos_abbr: Optional[str], special_mark: str = ""
) -> str:
    """Помета с учётом глоссария Novak (напр. mi: pl. → sing)."""
    if pos_abbr not in ("s.", "a.", "pron.", None):
        return special_mark
    book_tpl = _BOOK_TEMPLATE_OVERRIDES.get(lemma_clean(lemma).lower())
    if book_tpl:
        return book_tpl[0]
    return special_mark


def _pair(base: str, slot: Tuple[str, Optional[str]]) -> Tuple[str, str]:
    weak_sfx, strong_sfx = slot
    weak = apply_suffix(base, weak_sfx)
    if strong_sfx is None:
        return weak, weak
    return weak, apply_suffix(base, strong_sfx)


def _pairs(base: str, slot_alts: SlotAlts) -> List[Tuple[str, str]]:
    return [_pair(base, alt) for alt in slot_alts]


def _build_nominal(
    base: str, slots: Sequence[SlotAlts], mark: str
) -> StemMap:
    """
    Имя: слоты → (1:2), 3, (4:5).
    pl.  → только 4:5
    sing.→ только 1:2 и 3
    Альтернативы `/` обычно в слоте 4/5 — пары alt по индексу.
    """
    out: StemMap = {}

    if mark == "pl":
        if len(slots) >= 1:
            pairs = _pairs(base, slots[0])
            out[4] = [w for w, _ in pairs]
            out[5] = [s for _, s in pairs]
        return out

    if mark == "sing":
        if len(slots) >= 1:
            pairs = _pairs(base, slots[0])
            out[1] = [w for w, _ in pairs]
            out[2] = [s for _, s in pairs]
        if len(slots) >= 2:
            out[3] = [apply_suffix(base, slots[1][0][0])]
        return out

    if len(slots) >= 1:
        pairs = _pairs(base, slots[0])
        out[1] = [w for w, _ in pairs]
        out[2] = [s for _, s in pairs]
    if len(slots) >= 2:
        # partitive обычно без /; берём первую альт. weak
        out[3] = [apply_suffix(base, alt[0]) for alt in slots[1]]
    if len(slots) >= 3:
        pairs = _pairs(base, slots[2])
        out[4] = [w for w, _ in pairs]
        out[5] = [s for _, s in pairs]
    return out


def _build_verb(base: str, slots: Sequence[SlotAlts], mark: str) -> StemMap:
    """
    Глагол: 5 слотов → (1:2), (3:4), 5, 6, 7.
    v. def. → 2, 4, 5, 6, 7.
    """
    out: StemMap = {}

    if mark == "v_def":
        nums = (2, 4, 5, 6, 7)
        for i, num in enumerate(nums):
            if i >= len(slots):
                break
            pairs = _pairs(base, slots[i])
            # сильная (или единственная) по каждой альт.
            out[num] = [s for _, s in pairs]
        return out

    if len(slots) >= 1:
        pairs = _pairs(base, slots[0])
        out[1] = [w for w, _ in pairs]
        out[2] = [s for _, s in pairs]
    if len(slots) >= 2:
        pairs = _pairs(base, slots[1])
        out[3] = [w for w, _ in pairs]
        out[4] = [s for _, s in pairs]
    if len(slots) >= 3:
        out[5] = [apply_suffix(base, alt[0]) for alt in slots[2]]
    if len(slots) >= 4:
        out[6] = [apply_suffix(base, alt[0]) for alt in slots[3]]
    if len(slots) >= 5:
        out[7] = [apply_suffix(base, alt[0]) for alt in slots[4]]
    return out
