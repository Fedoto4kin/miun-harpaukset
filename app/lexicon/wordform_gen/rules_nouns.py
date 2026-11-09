"""
Правила склонения имён из Grammatika_karelia_proper_tver.doc.

Основы: 0=лемма, 1=слаб.ед, 2=сильн.ед, 3=парт.ед (готовая),
        4=слаб.мн, 5=сильн.мн.
"""

from __future__ import annotations

from typing import Callable, Dict, Optional

from .harmony import pick

# code → (нужно_число: "sg"|"pl"|"both", builder)
# builder(stems) → form | None

StemMap = Dict[int, str]


def _ends_with_i(stem: str) -> bool:
    return bool(stem) and stem[-1].lower() == "i"


def _ends_with_oi(stem: str) -> bool:
    low = stem.lower()
    return low.endswith("oi") or low.endswith("öi")


def build_noun_form(code: str, stems: StemMap) -> Optional[str]:
    """Строит одну словоформу по коду GrammarForm."""
    fn = _BUILDERS.get(code)
    if not fn:
        return None
    return fn(stems)


def _req(stems: StemMap, *nums: int) -> Optional[tuple]:
    vals = []
    for n in nums:
        v = stems.get(n)
        if not v:
            return None
        vals.append(v)
    return tuple(vals)


def _nom_sg(stems: StemMap) -> Optional[str]:
    return stems.get(0)


def _gen_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + "n"


def _part_sg(stems: StemMap) -> Optional[str]:
    return stems.get(3)


def _ess_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 2)
    if not s:
        return None
    return s[0] + pick(s[0], "na", "nä")


def _transl_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1, 2)
    if not s:
        return None
    s1, s2 = s
    return s1 + ("ksi" if _ends_with_i(s2) else "kši")


def _iness_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1, 2)
    if not s:
        return None
    s1, s2 = s
    if _ends_with_i(s2):
        return s1 + pick(s1, "ssa", "ssä")
    return s1 + pick(s1, "šša", "ššä")


def _elat_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1, 2)
    if not s:
        return None
    s1, s2 = s
    if _ends_with_i(s2):
        return s1 + pick(s1, "sta", "stä")
    return s1 + pick(s1, "šta", "štä")


def _ill_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 2)
    return None if not s else s[0] + "h"


def _ades_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    if not s:
        return None
    return s[0] + pick(s[0], "lla", "llä")


def _ablat_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    if not s:
        return None
    return s[0] + pick(s[0], "lda", "ldä")


def _abess_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    if not s:
        return None
    return s[0] + pick(s[0], "tta", "ttä")


def _com_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + "nke"


def _prol_sg(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + "čči"


def _nom_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + "t"


def _gen_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    return None if not s else s[0] + "n"


def _part_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 5)
    if not s:
        return None
    s5 = s[0]
    if _ends_with_oi(s5):
        return s5 + pick(s5, "da", "dä")
    return s5 + "e"


def _ess_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 5)
    if not s:
        return None
    return s[0] + pick(s[0], "na", "nä")


def _transl_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    return None if not s else s[0] + "ksi"


def _iness_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return s[0] + pick(s[0], "ssa", "ssä")


def _elat_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return s[0] + pick(s[0], "sta", "stä")


def _ill_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 5)
    return None if not s else s[0] + "h"


def _ades_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return s[0] + pick(s[0], "lla", "llä")


def _ablat_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return s[0] + pick(s[0], "lda", "ldä")


def _abess_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return s[0] + pick(s[0], "tta", "ttä")


def _com_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    return None if not s else s[0] + "nke"


def _prol_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    return None if not s else s[0] + "čči"


def _instr_pl(stems: StemMap) -> Optional[str]:
    s = _req(stems, 4)
    return None if not s else s[0] + "n"


_BUILDERS: Dict[str, Callable[[StemMap], Optional[str]]] = {
    "nom_sg": _nom_sg,
    "gen_sg": _gen_sg,
    "part_sg": _part_sg,
    "ess_sg": _ess_sg,
    "transl_sg": _transl_sg,
    "iness_sg": _iness_sg,
    "elat_sg": _elat_sg,
    "ill_sg": _ill_sg,
    "ades_sg": _ades_sg,
    "ablat_sg": _ablat_sg,
    "abess_sg": _abess_sg,
    "com_sg": _com_sg,
    "prol_sg": _prol_sg,
    "nom_pl": _nom_pl,
    "gen_pl": _gen_pl,
    "part_pl": _part_pl,
    "ess_pl": _ess_pl,
    "transl_pl": _transl_pl,
    "iness_pl": _iness_pl,
    "elat_pl": _elat_pl,
    "ill_pl": _ill_pl,
    "ades_pl": _ades_pl,
    "ablat_pl": _ablat_pl,
    "abess_pl": _abess_pl,
    "com_pl": _com_pl,
    "prol_pl": _prol_pl,
    "instr_pl": _instr_pl,
}

SG_CODES = tuple(c for c in _BUILDERS if c.endswith("_sg"))
PL_CODES = tuple(c for c in _BUILDERS if c.endswith("_pl"))
ALL_NOUN_CODES = SG_CODES + PL_CODES
