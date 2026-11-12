"""
Готовая парадигма отрицательного глагола ei (kield. v. / v. negat.).

Источник: Grammatika_karelia_proper_tver + учебник Novak.
Слоты — существующие GrammarForm verb (ind_pres_*_pos, imp_*_pos):
у ei это и есть полная парадигма (других времён у самого вспомогательного нет).
"""

from __future__ import annotations

from typing import Dict, Iterator, List, Tuple

LEMMA = "ei"
POS_ABBR = "v. negat."

# code → орфография
PARADIGM: Dict[str, str] = {
    "ind_pres_1sg_pos": "en",
    "ind_pres_2sg_pos": "et",
    "ind_pres_3sg_pos": "ei",
    "ind_pres_1pl_pos": "emmä",
    "ind_pres_2pl_pos": "että",
    "ind_pres_3pl_pos": "ei",
    "imp_2sg_pos": "elä",
    "imp_3sg_pos": "elgäh",
    "imp_2pl_pos": "elgiä",
    "imp_3pl_pos": "elgäh",
}


def iter_forms() -> Iterator[Tuple[str, str]]:
    """(grammar_form.code, form) в порядке PARADIGM."""
    for code, form in PARADIGM.items():
        yield code, form


def form_codes() -> List[str]:
    return list(PARADIGM.keys())
