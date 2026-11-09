"""Генерация парадигмы глагола (фазы 1–2) из словаря основ."""

from __future__ import annotations

from typing import Dict, List, Mapping, Sequence, Union

from .rules_verbs import (
    ALL_VERB_CODES,
    VDEF_VERB_CODES,
    build_verb_form,
)

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


def generate_verb_forms(
    stems: StemInput,
    lemma: str = "",
    special_mark: str = "",
) -> Dict[str, List[str]]:
    """
    stems: {0..7: form} или {0..7: [alt0, ...]}.
    lemma: начальная форма (для ветвлений ua/iä, ta/tä); если пусто — stems[0].

    Возвращает {grammar_form.code: [орфография, ...]}.
    """
    stem_lists = _normalize_stems(stems)
    if not stem_lists:
        return {}

    lemma = lemma or (stem_lists.get(0) or [""])[0]
    codes = VDEF_VERB_CODES if special_mark == "v_def" else ALL_VERB_CODES

    max_alts = max(len(forms) for forms in stem_lists.values())
    collected: Dict[str, List[str]] = {}

    for alt in range(max_alts):
        stem_map = {
            n: (forms[alt] if alt < len(forms) else forms[0])
            for n, forms in stem_lists.items()
        }
        for code in codes:
            form = build_verb_form(code, stem_map, lemma)
            if not form:
                continue
            bucket = collected.setdefault(code, [])
            if form not in bucket:
                bucket.append(form)

    return collected
