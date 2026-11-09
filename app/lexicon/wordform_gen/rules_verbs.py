"""
Правила глагольного словоизменения (фаза 1) из Grammatika_karelia_proper_tver.doc.

Слоты: индикатив презенс/имперфект, императив, кондиционал имперфект, I инф.
Форма 73 — по блок-схеме _grammatika_verb_cond73.png (не по обрезанному тексту).
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Sequence

from .harmony import is_back_harmony, pick

StemMap = Dict[int, str]

# Мягкий знак как в словарных основах (U+02BC)
SOFT = "\u02bc"

_VOWELS = set("aeiouyäöüAEIOUYÄÖÜ")


def _req(stems: StemMap, *nums: int) -> Optional[tuple]:
    vals = []
    for n in nums:
        v = stems.get(n)
        if not v:
            return None
        vals.append(v)
    return tuple(vals)


def _is_vowel(ch: str) -> bool:
    return ch in _VOWELS


def ends_cv(stem: str) -> bool:
    """Окончание «согласный + гласный» (CV)."""
    if len(stem) < 2:
        return False
    return (not _is_vowel(stem[-2])) and _is_vowel(stem[-1])


def ends_vv(stem: str) -> bool:
    """Окончание «два гласных» (VV / дифтонг)."""
    if len(stem) < 2:
        return False
    return _is_vowel(stem[-2]) and _is_vowel(stem[-1])


def lemma_ends_ua_ia(lemma: str) -> bool:
    low = lemma.lower()
    return low.endswith("ua") or low.endswith("iä")


def lemma_ends_ta_ta(lemma: str) -> bool:
    low = lemma.lower()
    return low.endswith("ta") or low.endswith("tä")


def uy(stem: str) -> str:
    return pick(stem, "u", "y")


def replace_final_e_to_o(stem: str) -> str:
    """Ce → Co/Cö: одиночный e после согласного."""
    if len(stem) >= 2 and stem[-1].lower() == "e" and not _is_vowel(stem[-2]):
        return stem[:-1] + pick(stem, "o", "ö")
    return stem


def cond_stem4_adjust(stem4: str, lemma: str) -> str:
    """
    Для конд. 1/2 л.: если лемма на ua/iä, последний гласный основы 4
    o или i → a/ä.
    """
    if not lemma_ends_ua_ia(lemma) or not stem4:
        return stem4
    last = stem4[-1]
    if last.lower() in ("o", "ö"):
        return stem4[:-1] + pick(stem4, "a", "ä")
    if last.lower() == "i":
        return stem4[:-1] + pick(stem4, "a", "ä")
    return stem4


def cond_imp_3sg(stem4: str, lemma: str) -> Optional[str]:
    """
    Форма 73 — блок-схема:
      основа 4 на i?
        да → лемма ua/iä? нет → +s' ; да → без послед. + a/ä + is'
        нет → лемма ua/iä и основа на o? да → без послед. + a + is' ; иначе + is'
    """
    if not stem4:
        return None
    soft_s = "s" + SOFT
    soft_is = "is" + SOFT
    ends_i = stem4[-1].lower() == "i"
    ua = lemma_ends_ua_ia(lemma)

    if ends_i:
        if not ua:
            return stem4 + soft_s
        # без последней + a/ä + is'
        return stem4[:-1] + pick(stem4, "a", "ä") + soft_is

    if ua and stem4[-1].lower() == "o":
        return stem4[:-1] + "a" + soft_is
    return stem4 + soft_is


def imperative_3_suffix(stem5: str, lemma: str) -> Optional[str]:
    """
    Формы 50/52: выбор суффикса по исходу основы 5.
    Возвращает полный суффикс для 3sg (kkah/…) или None.
    """
    if not stem5:
        return None
    last = stem5[-1].lower()

    # n + лемма на ta/tä → n>k + kah/käh
    if last == "n" and lemma_ends_ta_ta(lemma):
        return pick(stem5, "kah", "käh")

    if last in ("s", "š"):
        return pick(stem5, "kah", "käh")

    if last in ("l", "n", "r") or ends_vv(stem5):
        return pick(stem5, "gah", "gäh")

    if ends_cv(stem5):
        return pick(stem5, "kkah", "kkäh")

    # запасной: как CV
    return pick(stem5, "kkah", "kkäh")


def imperative_3_base(stem5: str, lemma: str) -> Optional[str]:
    """Основа перед суффиксом 3л. императива (n→k при ta/tä)."""
    if not stem5:
        return None
    if stem5[-1].lower() == "n" and lemma_ends_ta_ta(lemma):
        return stem5[:-1] + "k"
    return stem5


def imperative_2pl_suffix(stem5: str, lemma: str) -> Optional[str]:
    if not stem5:
        return None
    last = stem5[-1].lower()
    if last == "n" and lemma_ends_ta_ta(lemma):
        return pick(stem5, "kua", "kiä")
    if last in ("s", "š"):
        return pick(stem5, "kua", "kiä")
    if last in ("l", "n", "r") or ends_vv(stem5):
        return pick(stem5, "gua", "giä")
    if ends_cv(stem5):
        return pick(stem5, "kkua", "kkiä")
    return pick(stem5, "kkua", "kkiä")


# --- builders: (stems, lemma) -> form ---

Builder = Callable[[StemMap, str], Optional[str]]


def _ind_pres_1sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + "n"


def _ind_pres_2sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + "t"


def _ind_pres_3sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    if not s:
        return None
    base = replace_final_e_to_o(s[0])
    return base + uy(base)


def _ind_pres_1pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + pick(s[0], "mma", "mmä")


def _ind_pres_2pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0] + pick(s[0], "tta", "ttä")


def _ind_pres_3pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 6)
    return None if not s else s[0] + "h"


def _ind_pres_1sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else "en " + s[0]


def _ind_pres_2sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else "et " + s[0]


def _ind_pres_3sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else "ei " + s[0]


def _ind_pres_1pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else "emmä " + s[0]


def _ind_pres_2pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else "että " + s[0]


def _ind_pres_3pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 6)
    return None if not s else "ei " + s[0]


def _ind_imp_1sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 3)
    return None if not s else s[0] + "n"


def _ind_imp_2sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 3)
    return None if not s else s[0] + "t"


def _ind_imp_3sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    return None if not s else s[0]


def _ind_imp_1pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    st = s[0]
    if ends_vv(st):
        return st + pick(st, "mma", "mmä")
    if ends_cv(st):
        return st + pick(st, "ma", "mä")
    return st + pick(st, "ma", "mä")


def _ind_imp_2pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    st = s[0]
    if ends_vv(st):
        return st + pick(st, "tta", "ttä")
    if ends_cv(st):
        return st + pick(st, "ja", "jä")
    return st + pick(st, "ja", "jä")


def _ind_imp_3pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 7)
    return None if not s else s[0] + "ih"


def _ind_imp_3pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    """Форма 24: ei основа 7 + u/y (синтетика; 19–23 — аналитика, фаза 2)."""
    s = _req(stems, 7)
    if not s:
        return None
    return "ei " + s[0] + uy(s[0])


def _imp_2sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else s[0]


def _imp_3sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 5)
    if not s:
        return None
    base = imperative_3_base(s[0], lemma)
    sfx = imperative_3_suffix(s[0], lemma)
    if base is None or sfx is None:
        return None
    return base + sfx


def _imp_2pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 5)
    if not s:
        return None
    base = imperative_3_base(s[0], lemma)
    sfx = imperative_2pl_suffix(s[0], lemma)
    if base is None or sfx is None:
        return None
    return base + sfx


def _imp_3pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    return _imp_3sg_pos(stems, lemma)


def _imp_2sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 1)
    return None if not s else "elä " + s[0]


def _imp_3sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _imp_3sg_pos(stems, lemma)
    return None if not pos else "elgäh " + pos


def _imp_2pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _imp_2pl_pos(stems, lemma)
    return None if not pos else "elgiä " + pos


def _imp_3pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    return _imp_3sg_neg(stems, lemma)


def _cond_imp_1sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return cond_stem4_adjust(s[0], lemma) + "zin"


def _cond_imp_2sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return cond_stem4_adjust(s[0], lemma) + "zit"


def _cond_imp_3sg_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    return cond_imp_3sg(s[0], lemma)


def _cond_imp_1pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    st = cond_stem4_adjust(s[0], lemma)
    return st + pick(st, "zima", "zimä")


def _cond_imp_2pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 4)
    if not s:
        return None
    st = cond_stem4_adjust(s[0], lemma)
    return st + pick(st, "zija", "zijä")


def _cond_imp_3pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 7)
    if not s:
        return None
    return s[0] + pick(s[0], "ais" + SOFT, "äis" + SOFT)


def _cond_imp_1sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _cond_imp_3sg_pos(stems, lemma)
    return None if not pos else "en " + pos


def _cond_imp_2sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _cond_imp_3sg_pos(stems, lemma)
    return None if not pos else "et " + pos


def _cond_imp_3sg_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _cond_imp_3sg_pos(stems, lemma)
    return None if not pos else "ei " + pos


def _cond_imp_1pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _cond_imp_3sg_pos(stems, lemma)
    return None if not pos else "emmä " + pos


def _cond_imp_2pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _cond_imp_3sg_pos(stems, lemma)
    return None if not pos else "että " + pos


def _cond_imp_3pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    pos = _cond_imp_3pl_pos(stems, lemma)
    return None if not pos else "ei " + pos


def _inf1(stems: StemMap, lemma: str) -> Optional[str]:
    return stems.get(0) or lemma or None


def _init_builders() -> Dict[str, Builder]:
    return {
    # индикатив презенс +
    "ind_pres_1sg_pos": _ind_pres_1sg_pos,
    "ind_pres_2sg_pos": _ind_pres_2sg_pos,
    "ind_pres_3sg_pos": _ind_pres_3sg_pos,
    "ind_pres_1pl_pos": _ind_pres_1pl_pos,
    "ind_pres_2pl_pos": _ind_pres_2pl_pos,
    "ind_pres_3pl_pos": _ind_pres_3pl_pos,
    # индикатив презенс −
    "ind_pres_1sg_neg": _ind_pres_1sg_neg,
    "ind_pres_2sg_neg": _ind_pres_2sg_neg,
    "ind_pres_3sg_neg": _ind_pres_3sg_neg,
    "ind_pres_1pl_neg": _ind_pres_1pl_neg,
    "ind_pres_2pl_neg": _ind_pres_2pl_neg,
    "ind_pres_3pl_neg": _ind_pres_3pl_neg,
    # индикатив имперфект +
    "ind_impf_1sg_pos": _ind_imp_1sg_pos,
    "ind_impf_2sg_pos": _ind_imp_2sg_pos,
    "ind_impf_3sg_pos": _ind_imp_3sg_pos,
    "ind_impf_1pl_pos": _ind_imp_1pl_pos,
    "ind_impf_2pl_pos": _ind_imp_2pl_pos,
    "ind_impf_3pl_pos": _ind_imp_3pl_pos,
    # индикатив имперфект − (только 3pl синтетика)
    "ind_impf_3pl_neg": _ind_imp_3pl_neg,
    # императив
    "imp_2sg_pos": _imp_2sg_pos,
    "imp_3sg_pos": _imp_3sg_pos,
    "imp_2pl_pos": _imp_2pl_pos,
    "imp_3pl_pos": _imp_3pl_pos,
    "imp_2sg_neg": _imp_2sg_neg,
    "imp_3sg_neg": _imp_3sg_neg,
    "imp_2pl_neg": _imp_2pl_neg,
    "imp_3pl_neg": _imp_3pl_neg,
    # кондиционал имперфект
    "cond_impf_1sg_pos": _cond_imp_1sg_pos,
    "cond_impf_2sg_pos": _cond_imp_2sg_pos,
    "cond_impf_3sg_pos": _cond_imp_3sg_pos,
    "cond_impf_1pl_pos": _cond_imp_1pl_pos,
    "cond_impf_2pl_pos": _cond_imp_2pl_pos,
    "cond_impf_3pl_pos": _cond_imp_3pl_pos,
    "cond_impf_1sg_neg": _cond_imp_1sg_neg,
    "cond_impf_2sg_neg": _cond_imp_2sg_neg,
    "cond_impf_3sg_neg": _cond_imp_3sg_neg,
    "cond_impf_1pl_neg": _cond_imp_1pl_neg,
    "cond_impf_2pl_neg": _cond_imp_2pl_neg,
    "cond_impf_3pl_neg": _cond_imp_3pl_neg,
    # I инфинитив
    "inf1": _inf1,
    }


_BUILDERS: Dict[str, Builder] = _init_builders()

# Метаданные фазы 1
VERB_FORM_META: List[tuple] = [
    ("ind_pres_1sg_pos", "indikativa prezens 1.yks. myönteinen", "индикатив презенс 1л. ед. пол.", 100),
    ("ind_pres_2sg_pos", "indikativa prezens 2.yks. myönteinen", "индикатив презенс 2л. ед. пол.", 110),
    ("ind_pres_3sg_pos", "indikativa prezens 3.yks. myönteinen", "индикатив презенс 3л. ед. пол.", 120),
    ("ind_pres_1pl_pos", "indikativa prezens 1.mon. myönteinen", "индикатив презенс 1л. мн. пол.", 130),
    ("ind_pres_2pl_pos", "indikativa prezens 2.mon. myönteinen", "индикатив презенс 2л. мн. пол.", 140),
    ("ind_pres_3pl_pos", "indikativa prezens 3.mon. myönteinen", "индикатив презенс 3л. мн. пол.", 150),
    ("ind_pres_1sg_neg", "indikativa prezens 1.yks. kieltävä", "индикатив презенс 1л. ед. отр.", 160),
    ("ind_pres_2sg_neg", "indikativa prezens 2.yks. kieltävä", "индикатив презенс 2л. ед. отр.", 170),
    ("ind_pres_3sg_neg", "indikativa prezens 3.yks. kieltävä", "индикатив презенс 3л. ед. отр.", 180),
    ("ind_pres_1pl_neg", "indikativa prezens 1.mon. kieltävä", "индикатив презенс 1л. мн. отр.", 190),
    ("ind_pres_2pl_neg", "indikativa prezens 2.mon. kieltävä", "индикатив презенс 2л. мн. отр.", 200),
    ("ind_pres_3pl_neg", "indikativa prezens 3.mon. kieltävä", "индикатив презенс 3л. мн. отр.", 210),
    ("ind_impf_1sg_pos", "indikativa imperfekta 1.yks. myönteinen", "индикатив имперфект 1л. ед. пол.", 220),
    ("ind_impf_2sg_pos", "indikativa imperfekta 2.yks. myönteinen", "индикатив имперфект 2л. ед. пол.", 230),
    ("ind_impf_3sg_pos", "indikativa imperfekta 3.yks. myönteinen", "индикатив имперфект 3л. ед. пол.", 240),
    ("ind_impf_1pl_pos", "indikativa imperfekta 1.mon. myönteinen", "индикатив имперфект 1л. мн. пол.", 250),
    ("ind_impf_2pl_pos", "indikativa imperfekta 2.mon. myönteinen", "индикатив имперфект 2л. мн. пол.", 260),
    ("ind_impf_3pl_pos", "indikativa imperfekta 3.mon. myönteinen", "индикатив имперфект 3л. мн. пол.", 270),
    ("ind_impf_3pl_neg", "indikativa imperfekta 3.mon. kieltävä", "индикатив имперфект 3л. мн. отр.", 280),
    ("imp_2sg_pos", "imperativa 2.yks. myönteinen", "императив 2л. ед. пол.", 300),
    ("imp_3sg_pos", "imperativa 3.yks. myönteinen", "императив 3л. ед. пол.", 310),
    ("imp_2pl_pos", "imperativa 2.mon. myönteinen", "императив 2л. мн. пол.", 320),
    ("imp_3pl_pos", "imperativa 3.mon. myönteinen", "императив 3л. мн. пол.", 330),
    ("imp_2sg_neg", "imperativa 2.yks. kieltävä", "императив 2л. ед. отр.", 340),
    ("imp_3sg_neg", "imperativa 3.yks. kieltävä", "императив 3л. ед. отр.", 350),
    ("imp_2pl_neg", "imperativa 2.mon. kieltävä", "императив 2л. мн. отр.", 360),
    ("imp_3pl_neg", "imperativa 3.mon. kieltävä", "императив 3л. мн. отр.", 370),
    ("cond_impf_1sg_pos", "konditsionala imperfekta 1.yks. myönteinen", "кондиционал имперфект 1л. ед. пол.", 400),
    ("cond_impf_2sg_pos", "konditsionala imperfekta 2.yks. myönteinen", "кондиционал имперфект 2л. ед. пол.", 410),
    ("cond_impf_3sg_pos", "konditsionala imperfekta 3.yks. myönteinen", "кондиционал имперфект 3л. ед. пол.", 420),
    ("cond_impf_1pl_pos", "konditsionala imperfekta 1.mon. myönteinen", "кондиционал имперфект 1л. мн. пол.", 430),
    ("cond_impf_2pl_pos", "konditsionala imperfekta 2.mon. myönteinen", "кондиционал имперфект 2л. мн. пол.", 440),
    ("cond_impf_3pl_pos", "konditsionala imperfekta 3.mon. myönteinen", "кондиционал имперфект 3л. мн. пол.", 450),
    ("cond_impf_1sg_neg", "konditsionala imperfekta 1.yks. kieltävä", "кондиционал имперфект 1л. ед. отр.", 460),
    ("cond_impf_2sg_neg", "konditsionala imperfekta 2.yks. kieltävä", "кондиционал имперфект 2л. ед. отр.", 470),
    ("cond_impf_3sg_neg", "konditsionala imperfekta 3.yks. kieltävä", "кондиционал имперфект 3л. ед. отр.", 480),
    ("cond_impf_1pl_neg", "konditsionala imperfekta 1.mon. kieltävä", "кондиционал имперфект 1л. мн. отр.", 490),
    ("cond_impf_2pl_neg", "konditsionala imperfekta 2.mon. kieltävä", "кондиционал имперфект 2л. мн. отр.", 500),
    ("cond_impf_3pl_neg", "konditsionala imperfekta 3.mon. kieltävä", "кондиционал имперфект 3л. мн. отр.", 510),
    ("inf1", "I infinitiva", "I инфинитив", 600),
]

# Подмешать фазу 2
from .rules_verbs_phase2 import PHASE2_BUILDERS, PHASE2_META  # noqa: E402

_BUILDERS.update(PHASE2_BUILDERS)
VERB_FORM_META.extend(PHASE2_META)

_NONFINITE_PREFIXES = ("inf", "part_")
_VDEF_CODES = frozenset(
    c
    for c in _BUILDERS
    if "_3sg_" in c
    or "_3pl_" in c
    or c.startswith(_NONFINITE_PREFIXES)
    or c == "inf1"
)

ALL_VERB_CODES: Sequence[str] = tuple(_BUILDERS.keys())
VDEF_VERB_CODES: Sequence[str] = tuple(c for c in ALL_VERB_CODES if c in _VDEF_CODES)


def build_verb_form(code: str, stems: StemMap, lemma: str) -> Optional[str]:
    fn = _BUILDERS.get(code)
    if not fn:
        return None
    return fn(stems, lemma)
