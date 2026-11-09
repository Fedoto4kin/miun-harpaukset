"""Генерация парадигмы существительного из словаря основ."""

from __future__ import annotations

from typing import Dict, List, Mapping, Sequence, Union

from .rules_nouns import ALL_NOUN_CODES, PL_CODES, SG_CODES, build_noun_form

StemInput = Mapping[int, Union[str, Sequence[str]]]


def _normalize_stems(stems: StemInput) -> Dict[int, List[str]]:
    out: Dict[int, List[str]] = {}
    for k, v in stems.items():
        n = int(k)
        if isinstance(v, str):
            if v:
                out[n] = [v]
        else:
            forms = [f for f in v if f]
            if forms:
                out[n] = forms
    return out


def generate_noun_forms(
    stems: StemInput,
    special_mark: str = "",
) -> Dict[str, List[str]]:
    """
    stems: {0..5: form} или {0..5: [alt0, alt1, ...]}.
    Альтернативы с одним индексом образуют одну парадигму (не декартово).

    Возвращает {grammar_form.code: [орфография, ...]}.
    """
    stem_lists = _normalize_stems(stems)
    if not stem_lists:
        return {}

    if special_mark == "pl":
        codes = PL_CODES
    elif special_mark == "sing":
        codes = SG_CODES
    else:
        codes = ALL_NOUN_CODES

    max_alts = max(len(forms) for forms in stem_lists.values())
    collected: Dict[str, List[str]] = {}

    for alt in range(max_alts):
        stem_map = {
            n: (forms[alt] if alt < len(forms) else forms[0])
            for n, forms in stem_lists.items()
        }
        for code in codes:
            form = build_noun_form(code, stem_map)
            if not form:
                continue
            bucket = collected.setdefault(code, [])
            if form not in bucket:
                bucket.append(form)

    return collected
