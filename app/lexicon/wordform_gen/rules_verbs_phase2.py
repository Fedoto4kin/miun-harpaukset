"""
Глаголы фаза 2: причастия, потенциал презенс, инф. II–III, аналитика на слоте 141.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Tuple

from .harmony import pick

# Локальные копии (без импорта rules_verbs — иначе цикл).
SOFT = "\u02bc"
_VOWELS = set("aeiouyäöüAEIOUYÄÖÜ")
StemMap = Dict[int, str]
Builder = Callable[[StemMap, str], Optional[str]]


def _is_vowel(ch: str) -> bool:
    return ch in _VOWELS


def _req(stems: StemMap, *nums: int) -> Optional[tuple]:
    vals = []
    for n in nums:
        v = stems.get(n)
        if not v:
            return None
        vals.append(v)
    return tuple(vals)


def ends_cv(stem: str) -> bool:
    if len(stem) < 2:
        return False
    return (not _is_vowel(stem[-2])) and _is_vowel(stem[-1])


def ends_vv(stem: str) -> bool:
    if len(stem) < 2:
        return False
    return _is_vowel(stem[-2]) and _is_vowel(stem[-1])


def uy(stem: str) -> str:
    return pick(stem, "u", "y")


# --- основа 5: суффиксы причастия / потенциала ---


def _stem5_class(stem5: str) -> str:
    """Класс исхода основы 5: cv | vv_n | l | r | s | sh | n | other."""
    if not stem5:
        return "other"
    last = stem5[-1].lower()
    if last == "l":
        return "l"
    if last == "r":
        return "r"
    if last == "s":
        return "s"
    if last == "š":
        return "sh"
    if last == "n":
        return "n"
    if ends_vv(stem5):
        return "vv_n"
    if ends_cv(stem5):
        return "cv"
    return "other"


def part_act2_full(stem5: str) -> Optional[str]:
    """Форма 140: актив 2-е причастие (полная). Гармония u/y по основе."""
    if not stem5:
        return None
    cls = _stem5_class(stem5)
    if cls == "cv":
        return stem5 + pick(stem5, "nnun", "nnyn")
    if cls in ("vv_n", "n"):
        return stem5 + pick(stem5, "nun", "nyn")
    if cls == "l":
        return stem5 + pick(stem5, "lun", "lyn")
    if cls == "r":
        return stem5 + pick(stem5, "run", "ryn")
    if cls == "s":
        return stem5 + pick(stem5, "sun", "syn")
    if cls == "sh":
        return stem5 + pick(stem5, "šun", "šyn")
    return stem5 + pick(stem5, "nnun", "nnyn")


def part_act2_short(stem5: str) -> Optional[str]:
    """Форма 141: краткое 2-е причастие = «перфект (форма основного глагола)»."""
    if not stem5:
        return None
    cls = _stem5_class(stem5)
    if cls == "cv":
        return stem5 + "n"
    if cls in ("vv_n", "n"):
        return stem5 + pick(stem5, "nun", "nyn")
    if cls == "l":
        return stem5 + pick(stem5, "lun", "lyn")
    if cls == "r":
        return stem5 + pick(stem5, "run", "ryn")
    if cls == "s":
        return stem5 + pick(stem5, "sun", "syn")
    if cls == "sh":
        return stem5 + pick(stem5, "šun", "šyn")
    return stem5 + "n"


def _perfect(stems: StemMap) -> Optional[str]:
    s5 = stems.get(5)
    return part_act2_short(s5) if s5 else None


def _pass_u(stems: StemMap) -> Optional[str]:
    """основа 7 + u/y."""
    s = _req(stems, 7)
    if not s:
        return None
    return s[0] + uy(s[0])


# Потенциал: суффиксы по классу основы 5
_POT_POS = {
    # kind -> {class: suffix} ; harmony pairs as (back, front) tuples where needed
    "1sg": {
        "cv": "nnen",
        "vv_n": "nnen",
        "l": "len",
        "r": "ren",
        "s": "sen",
        "sh": "šen",
        "n": "nen",
        "other": "nnen",
    },
    "2sg": {
        "cv": "nnet",
        "vv_n": "nnet",
        "l": "let",
        "r": "ret",
        "s": "set",
        "sh": "šet",
        "n": "net",
        "other": "nnet",
    },
    "3sg": {
        "cv": ("nnou", "nnöy"),
        "vv_n": ("nnou", "nnöy"),
        "l": ("lou", "löy"),
        "r": ("rou", "röy"),
        "s": ("sou", "söy"),
        "sh": ("šou", "šöy"),
        "n": ("nou", "nöy"),
        "other": ("nnou", "nnöy"),
    },
    "1pl": {
        "cv": ("nnemma", "nnemmä"),
        "vv_n": ("nnemma", "nnemmä"),
        "l": ("lemma", "lemmä"),
        "r": ("remma", "remmä"),
        "s": ("semma", "semmä"),
        "sh": ("šemma", "šemmä"),
        "n": ("nemma", "nemmä"),
        "other": ("nnemma", "nnemmä"),
    },
    "2pl": {
        "cv": ("nnetta", "nnettä"),
        "vv_n": ("nnetta", "nnettä"),
        "l": ("letta", "lettä"),
        "r": ("retta", "rettä"),
        "s": ("setta", "settä"),
        "sh": ("šetta", "šettä"),
        "n": ("netta", "nettä"),
        "other": ("nnetta", "nnettä"),
    },
    "neg": {
        "cv": "nne",
        "vv_n": "nne",
        "l": "le",
        "r": "re",
        "s": "se",
        "sh": "še",
        "n": "ne",
        "other": "nne",
    },
}


def _pot_sfx(stem5: str, kind: str) -> Optional[str]:
    cls = _stem5_class(stem5)
    table = _POT_POS[kind]
    raw = table.get(cls, table["other"])
    if isinstance(raw, tuple):
        return pick(stem5, raw[0], raw[1])
    return raw


def _pot_from_stem5(stems: StemMap, kind: str, neg_prefix: str = "") -> Optional[str]:
    s = _req(stems, 5)
    if not s:
        return None
    sfx = _pot_sfx(s[0], kind)
    if sfx is None:
        return None
    body = s[0] + sfx
    return f"{neg_prefix}{body}" if neg_prefix else body


# --- II инфинитив ---


def _lemma_for_inf2(lemma: str) -> str:
    """Ca/Cä → Ce перед суффиксами II инф."""
    if len(lemma) >= 2 and not _is_vowel(lemma[-2]) and lemma[-1].lower() in ("a", "ä"):
        return lemma[:-1] + "e"
    return lemma


def _inf2_iness(stems: StemMap, lemma: str) -> Optional[str]:
    lem = stems.get(0) or lemma
    if not lem:
        return None
    if ends_vv(lem):
        # s's'a / ssä — в корпусе anduas's'a
        return lem + pick(lem, f"s{SOFT}s{SOFT}a", f"s{SOFT}s{SOFT}ä")
    # Ca/Cä → e + šša/ššä
    base = _lemma_for_inf2(lem)
    if base != lem or (len(lem) >= 2 and not _is_vowel(lem[-2]) and lem[-1].lower() in ("a", "ä")):
        return base + pick(base, "šša", "ššä")
    # прочие (на согласный и т.п.) — как VV-мягкий вариант не применяем; + šša по умолчанию?
    # Grammatika описывает только VV и Ca/Cä. Для tulla (согласный): tullessa в фин.; в тверском часто + šša после e-перехода нет.
    # Dictorpus: tullessa? проверим позже. Пока: если заканчивается на согласный — + ašša? 
    # Практично: VV уже покрыт; иначе если ends with a/ä after C handled; else append šša/ššä to lemma as-is.
    return lem + pick(lem, "šša", "ššä")


def _inf2_instr(stems: StemMap, lemma: str) -> Optional[str]:
    lem = stems.get(0) or lemma
    if not lem:
        return None
    base = _lemma_for_inf2(lem)
    return base + "n"


# --- builders ---


def _part_act1(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    if not s:
        return None
    st = s[0]
    # Ce → Ci
    if len(st) >= 2 and st[-1].lower() == "e" and not _is_vowel(st[-2]):
        st = st[:-1] + "i"
    return st + pick(st, "ja", "jä")


def _part_act2(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 5)
    return part_act2_full(s[0]) if s else None


def _part_act2_short(stems: StemMap, lemma: str) -> Optional[str]:
    return _perfect(stems)


def _part_pass1(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 7)
    if not s:
        return None
    return s[0] + pick(s[0], "ava", "ävä")


def _part_pass2(stems: StemMap, lemma: str) -> Optional[str]:
    return _pass_u(stems)


def _inf3_ades(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    return None if not s else s[0] + pick(s[0], "malla", "mällä")


def _inf3_ill(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    return None if not s else s[0] + pick(s[0], "mah", "mäh")


def _inf3_iness(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    return None if not s else s[0] + pick(s[0], "mašša", "mäššä")


def _inf3_elat(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    return None if not s else s[0] + pick(s[0], "mašta", "mäštä")


def _inf3_abess(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 2)
    return None if not s else s[0] + pick(s[0], "matta", "mättä")


def _pot_pres_3pl_pos(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 7)
    if not s:
        return None
    return s[0] + pick(s[0], "anneh", "änneh")


def _pot_pres_3pl_neg(stems: StemMap, lemma: str) -> Optional[str]:
    s = _req(stems, 7)
    if not s:
        return None
    return "ei " + s[0] + pick(s[0], "anne", "änne")


def _with_perfect(prefix: str, stems: StemMap) -> Optional[str]:
    p = _perfect(stems)
    return None if not p else f"{prefix} {p}"


def _with_pass_u(prefix: str, stems: StemMap) -> Optional[str]:
    p = _pass_u(stems)
    return None if not p else f"{prefix} {p}"


PHASE2_BUILDERS: Dict[str, Builder] = {
    # причастия
    "part_act1": _part_act1,
    "part_act2": _part_act2,
    "part_act2_short": _part_act2_short,
    "part_pass1": _part_pass1,
    "part_pass2": _part_pass2,
    # инф. II–III
    "inf2_iness": _inf2_iness,
    "inf2_instr": _inf2_instr,
    "inf3_ades": _inf3_ades,
    "inf3_ill": _inf3_ill,
    "inf3_iness": _inf3_iness,
    "inf3_elat": _inf3_elat,
    "inf3_abess": _inf3_abess,
    # потенциал презенс +
    "pot_pres_1sg_pos": lambda st, lem: _pot_from_stem5(st, "1sg"),
    "pot_pres_2sg_pos": lambda st, lem: _pot_from_stem5(st, "2sg"),
    "pot_pres_3sg_pos": lambda st, lem: _pot_from_stem5(st, "3sg"),
    "pot_pres_1pl_pos": lambda st, lem: _pot_from_stem5(st, "1pl"),
    "pot_pres_2pl_pos": lambda st, lem: _pot_from_stem5(st, "2pl"),
    "pot_pres_3pl_pos": _pot_pres_3pl_pos,
    # потенциал презенс −
    "pot_pres_1sg_neg": lambda st, lem: _pot_from_stem5(st, "neg", "en "),
    "pot_pres_2sg_neg": lambda st, lem: _pot_from_stem5(st, "neg", "et "),
    "pot_pres_3sg_neg": lambda st, lem: _pot_from_stem5(st, "neg", "ei "),
    "pot_pres_1pl_neg": lambda st, lem: _pot_from_stem5(st, "neg", "emmä "),
    "pot_pres_2pl_neg": lambda st, lem: _pot_from_stem5(st, "neg", "että "),
    "pot_pres_3pl_neg": _pot_pres_3pl_neg,
    # инд. имперфект отр. 19–23 (24 уже в фазе 1)
    "ind_impf_1sg_neg": lambda st, lem: _with_perfect("en", st),
    "ind_impf_2sg_neg": lambda st, lem: _with_perfect("et", st),
    "ind_impf_3sg_neg": lambda st, lem: _with_perfect("ei", st),
    "ind_impf_1pl_neg": lambda st, lem: _with_perfect("emmä", st),
    "ind_impf_2pl_neg": lambda st, lem: _with_perfect("että", st),
    # инд. перфект
    "ind_perf_1sg_pos": lambda st, lem: _with_perfect("olen", st),
    "ind_perf_2sg_pos": lambda st, lem: _with_perfect("olet", st),
    "ind_perf_3sg_pos": lambda st, lem: _with_perfect("on", st),
    "ind_perf_1pl_pos": lambda st, lem: _with_perfect("olemma", st),
    "ind_perf_2pl_pos": lambda st, lem: _with_perfect("oletta", st),
    "ind_perf_3pl_pos": lambda st, lem: _with_pass_u("on", st),
    "ind_perf_1sg_neg": lambda st, lem: _with_perfect("en ole", st),
    "ind_perf_2sg_neg": lambda st, lem: _with_perfect("et ole", st),
    "ind_perf_3sg_neg": lambda st, lem: _with_perfect("ei ole", st),
    "ind_perf_1pl_neg": lambda st, lem: _with_perfect("emmä ole", st),
    "ind_perf_2pl_neg": lambda st, lem: _with_perfect("että ole", st),
    "ind_perf_3pl_neg": lambda st, lem: _with_pass_u("ei ole", st),
    # инд. плюсквамперфект
    "ind_plup_1sg_pos": lambda st, lem: _with_perfect("olin", st),
    "ind_plup_2sg_pos": lambda st, lem: _with_perfect("olit", st),
    "ind_plup_3sg_pos": lambda st, lem: _with_perfect("oli", st),
    "ind_plup_1pl_pos": lambda st, lem: _with_perfect("olima", st),
    "ind_plup_2pl_pos": lambda st, lem: _with_perfect("olija", st),
    "ind_plup_3pl_pos": lambda st, lem: _with_pass_u("oldih", st),
    "ind_plup_1sg_neg": lambda st, lem: _with_perfect("en ollun", st),
    "ind_plup_2sg_neg": lambda st, lem: _with_perfect("et ollun", st),
    "ind_plup_3sg_neg": lambda st, lem: _with_perfect("ei ollun", st),
    "ind_plup_1pl_neg": lambda st, lem: _with_perfect("emmä ollun", st),
    "ind_plup_2pl_neg": lambda st, lem: _with_perfect("että ollun", st),
    "ind_plup_3pl_neg": lambda st, lem: _with_pass_u("ei oldu", st),
    # конд. плюсквамперфект
    "cond_plup_1sg_pos": lambda st, lem: _with_perfect("olizin", st),
    "cond_plup_2sg_pos": lambda st, lem: _with_perfect("olizit", st),
    "cond_plup_3sg_pos": lambda st, lem: _with_perfect(f"olis{SOFT}", st),
    "cond_plup_1pl_pos": lambda st, lem: _with_perfect("olizima", st),
    "cond_plup_2pl_pos": lambda st, lem: _with_perfect("olizija", st),
    "cond_plup_3pl_pos": lambda st, lem: _with_pass_u(f"olis{SOFT}", st),
    "cond_plup_1sg_neg": lambda st, lem: _with_perfect(f"en olis{SOFT}", st),
    "cond_plup_2sg_neg": lambda st, lem: _with_perfect(f"et olis{SOFT}", st),
    "cond_plup_3sg_neg": lambda st, lem: _with_perfect(f"ei olis{SOFT}", st),
    "cond_plup_1pl_neg": lambda st, lem: _with_perfect(f"emmä olis{SOFT}", st),
    "cond_plup_2pl_neg": lambda st, lem: _with_perfect(f"että olis{SOFT}", st),
    "cond_plup_3pl_neg": lambda st, lem: _with_pass_u(f"ei olis{SOFT}", st),
    # потенциал перфект
    "pot_perf_1sg_pos": lambda st, lem: _with_perfect("lienen", st),
    "pot_perf_2sg_pos": lambda st, lem: _with_perfect("lienet", st),
    "pot_perf_3sg_pos": lambda st, lem: _with_perfect("lienöy", st),
    "pot_perf_1pl_pos": lambda st, lem: _with_perfect("lienemmä", st),
    "pot_perf_2pl_pos": lambda st, lem: _with_perfect("lienettä", st),
    "pot_perf_3pl_pos": lambda st, lem: _with_pass_u("lienöy", st),
    "pot_perf_1sg_neg": lambda st, lem: _with_perfect("en liene", st),
    "pot_perf_2sg_neg": lambda st, lem: _with_perfect("et liene", st),
    "pot_perf_3sg_neg": lambda st, lem: _with_perfect("ei liene", st),
    "pot_perf_1pl_neg": lambda st, lem: _with_perfect("emmä liene", st),
    "pot_perf_2pl_neg": lambda st, lem: _with_perfect("että liene", st),
    "pot_perf_3pl_neg": lambda st, lem: _with_pass_u("ei liene", st),
}

PHASE2_META: List[Tuple[str, str, str, int]] = [
    ("part_act1", "1. partitsiipa aktiiva", "актив 1-е причастие", 700),
    ("part_act2", "2. partitsiipa aktiiva", "актив 2-е причастие", 710),
    ("part_act2_short", "2. partitsiipa aktiiva lyhyt / perfekta", "актив 2-е причастие кратк. / перфект", 720),
    ("part_pass1", "1. partitsiipa passiiva", "пассив 1-е причастие", 730),
    ("part_pass2", "2. partitsiipa passiiva", "пассив 2-е причастие", 740),
    ("inf2_iness", "II infinitiva inessiva", "II инфинитив инессив", 610),
    ("inf2_instr", "II infinitiva instruktiiva", "II инфинитив инструктив", 620),
    ("inf3_ades", "III infinitiva adessiva", "III инфинитив адессив", 630),
    ("inf3_ill", "III infinitiva illativa", "III инфинитив иллатив", 640),
    ("inf3_iness", "III infinitiva inessiva", "III инфинитив инессив", 650),
    ("inf3_elat", "III infinitiva elativa", "III инфинитив элатив", 660),
    ("inf3_abess", "III infinitiva abessiva", "III инфинитив абессив", 670),
    ("pot_pres_1sg_pos", "potentiala prezensa 1.yks. myönteinen", "потенциал презенс 1л. ед. пол.", 800),
    ("pot_pres_2sg_pos", "potentiala prezensa 2.yks. myönteinen", "потенциал презенс 2л. ед. пол.", 810),
    ("pot_pres_3sg_pos", "potentiala prezensa 3.yks. myönteinen", "потенциал презенс 3л. ед. пол.", 820),
    ("pot_pres_1pl_pos", "potentiala prezensa 1.mon. myönteinen", "потенциал презенс 1л. мн. пол.", 830),
    ("pot_pres_2pl_pos", "potentiala prezensa 2.mon. myönteinen", "потенциал презенс 2л. мн. пол.", 840),
    ("pot_pres_3pl_pos", "potentiala prezensa 3.mon. myönteinen", "потенциал презенс 3л. мн. пол.", 850),
    ("pot_pres_1sg_neg", "potentiala prezensa 1.yks. kieltävä", "потенциал презенс 1л. ед. отр.", 860),
    ("pot_pres_2sg_neg", "potentiala prezensa 2.yks. kieltävä", "потенциал презенс 2л. ед. отр.", 870),
    ("pot_pres_3sg_neg", "potentiala prezensa 3.yks. kieltävä", "потенциал презенс 3л. ед. отр.", 880),
    ("pot_pres_1pl_neg", "potentiala prezensa 1.mon. kieltävä", "потенциал презенс 1л. мн. отр.", 890),
    ("pot_pres_2pl_neg", "potentiala prezensa 2.mon. kieltävä", "потенциал презенс 2л. мн. отр.", 900),
    ("pot_pres_3pl_neg", "potentiala prezensa 3.mon. kieltävä", "потенциал презенс 3л. мн. отр.", 910),
    ("ind_impf_1sg_neg", "indikativa imperfekta 1.yks. kieltävä", "индикатив имперфект 1л. ед. отр.", 271),
    ("ind_impf_2sg_neg", "indikativa imperfekta 2.yks. kieltävä", "индикатив имперфект 2л. ед. отр.", 272),
    ("ind_impf_3sg_neg", "indikativa imperfekta 3.yks. kieltävä", "индикатив имперфект 3л. ед. отр.", 273),
    ("ind_impf_1pl_neg", "indikativa imperfekta 1.mon. kieltävä", "индикатив имперфект 1л. мн. отр.", 274),
    ("ind_impf_2pl_neg", "indikativa imperfekta 2.mon. kieltävä", "индикатив имперфект 2л. мн. отр.", 275),
    ("ind_perf_1sg_pos", "indikativa perfekta 1.yks. myönteinen", "индикатив перфект 1л. ед. пол.", 1000),
    ("ind_perf_2sg_pos", "indikativa perfekta 2.yks. myönteinen", "индикатив перфект 2л. ед. пол.", 1010),
    ("ind_perf_3sg_pos", "indikativa perfekta 3.yks. myönteinen", "индикатив перфект 3л. ед. пол.", 1020),
    ("ind_perf_1pl_pos", "indikativa perfekta 1.mon. myönteinen", "индикатив перфект 1л. мн. пол.", 1030),
    ("ind_perf_2pl_pos", "indikativa perfekta 2.mon. myönteinen", "индикатив перфект 2л. мн. пол.", 1040),
    ("ind_perf_3pl_pos", "indikativa perfekta 3.mon. myönteinen", "индикатив перфект 3л. мн. пол.", 1050),
    ("ind_perf_1sg_neg", "indikativa perfekta 1.yks. kieltävä", "индикатив перфект 1л. ед. отр.", 1060),
    ("ind_perf_2sg_neg", "indikativa perfekta 2.yks. kieltävä", "индикатив перфект 2л. ед. отр.", 1070),
    ("ind_perf_3sg_neg", "indikativa perfekta 3.yks. kieltävä", "индикатив перфект 3л. ед. отр.", 1080),
    ("ind_perf_1pl_neg", "indikativa perfekta 1.mon. kieltävä", "индикатив перфект 1л. мн. отр.", 1090),
    ("ind_perf_2pl_neg", "indikativa perfekta 2.mon. kieltävä", "индикатив перфект 2л. мн. отр.", 1100),
    ("ind_perf_3pl_neg", "indikativa perfekta 3.mon. kieltävä", "индикатив перфект 3л. мн. отр.", 1110),
    ("ind_plup_1sg_pos", "indikativa pluskvamperfekta 1.yks. myönteinen", "индикатив плюсквамперфект 1л. ед. пол.", 1200),
    ("ind_plup_2sg_pos", "indikativa pluskvamperfekta 2.yks. myönteinen", "индикатив плюсквамперфект 2л. ед. пол.", 1210),
    ("ind_plup_3sg_pos", "indikativa pluskvamperfekta 3.yks. myönteinen", "индикатив плюсквамперфект 3л. ед. пол.", 1220),
    ("ind_plup_1pl_pos", "indikativa pluskvamperfekta 1.mon. myönteinen", "индикатив плюсквамперфект 1л. мн. пол.", 1230),
    ("ind_plup_2pl_pos", "indikativa pluskvamperfekta 2.mon. myönteinen", "индикатив плюсквамперфект 2л. мн. пол.", 1240),
    ("ind_plup_3pl_pos", "indikativa pluskvamperfekta 3.mon. myönteinen", "индикатив плюсквамперфект 3л. мн. пол.", 1250),
    ("ind_plup_1sg_neg", "indikativa pluskvamperfekta 1.yks. kieltävä", "индикатив плюсквамперфект 1л. ед. отр.", 1260),
    ("ind_plup_2sg_neg", "indikativa pluskvamperfekta 2.yks. kieltävä", "индикатив плюсквамперфект 2л. ед. отр.", 1270),
    ("ind_plup_3sg_neg", "indikativa pluskvamperfekta 3.yks. kieltävä", "индикатив плюсквамперфект 3л. ед. отр.", 1280),
    ("ind_plup_1pl_neg", "indikativa pluskvamperfekta 1.mon. kieltävä", "индикатив плюсквамперфект 1л. мн. отр.", 1290),
    ("ind_plup_2pl_neg", "indikativa pluskvamperfekta 2.mon. kieltävä", "индикатив плюсквамперфект 2л. мн. отр.", 1300),
    ("ind_plup_3pl_neg", "indikativa pluskvamperfekta 3.mon. kieltävä", "индикатив плюсквамперфект 3л. мн. отр.", 1310),
    ("cond_plup_1sg_pos", "konditsionala pluskvamperfekta 1.yks. myönteinen", "кондиционал плюсквамперфект 1л. ед. пол.", 1400),
    ("cond_plup_2sg_pos", "konditsionala pluskvamperfekta 2.yks. myönteinen", "кондиционал плюсквамперфект 2л. ед. пол.", 1410),
    ("cond_plup_3sg_pos", "konditsionala pluskvamperfekta 3.yks. myönteinen", "кондиционал плюсквамперфект 3л. ед. пол.", 1420),
    ("cond_plup_1pl_pos", "konditsionala pluskvamperfekta 1.mon. myönteinen", "кондиционал плюсквамперфект 1л. мн. пол.", 1430),
    ("cond_plup_2pl_pos", "konditsionala pluskvamperfekta 2.mon. myönteinen", "кондиционал плюсквамперфект 2л. мн. пол.", 1440),
    ("cond_plup_3pl_pos", "konditsionala pluskvamperfekta 3.mon. myönteinen", "кондиционал плюсквамперфект 3л. мн. пол.", 1450),
    ("cond_plup_1sg_neg", "konditsionala pluskvamperfekta 1.yks. kieltävä", "кондиционал плюсквамперфект 1л. ед. отр.", 1460),
    ("cond_plup_2sg_neg", "konditsionala pluskvamperfekta 2.yks. kieltävä", "кондиционал плюсквамперфект 2л. ед. отр.", 1470),
    ("cond_plup_3sg_neg", "konditsionala pluskvamperfekta 3.yks. kieltävä", "кондиционал плюсквамперфект 3л. ед. отр.", 1480),
    ("cond_plup_1pl_neg", "konditsionala pluskvamperfekta 1.mon. kieltävä", "кондиционал плюсквамперфект 1л. мн. отр.", 1490),
    ("cond_plup_2pl_neg", "konditsionala pluskvamperfekta 2.mon. kieltävä", "кондиционал плюсквамперфект 2л. мн. отр.", 1500),
    ("cond_plup_3pl_neg", "konditsionala pluskvamperfekta 3.mon. kieltävä", "кондиционал плюсквамперфект 3л. мн. отр.", 1510),
    ("pot_perf_1sg_pos", "potentiala perfekta 1.yks. myönteinen", "потенциал перфект 1л. ед. пол.", 1600),
    ("pot_perf_2sg_pos", "potentiala perfekta 2.yks. myönteinen", "потенциал перфект 2л. ед. пол.", 1610),
    ("pot_perf_3sg_pos", "potentiala perfekta 3.yks. myönteinen", "потенциал перфект 3л. ед. пол.", 1620),
    ("pot_perf_1pl_pos", "potentiala perfekta 1.mon. myönteinen", "потенциал перфект 1л. мн. пол.", 1630),
    ("pot_perf_2pl_pos", "potentiala perfekta 2.mon. myönteinen", "потенциал перфект 2л. мн. пол.", 1640),
    ("pot_perf_3pl_pos", "potentiala perfekta 3.mon. myönteinen", "потенциал перфект 3л. мн. пол.", 1650),
    ("pot_perf_1sg_neg", "potentiala perfekta 1.yks. kieltävä", "потенциал перфект 1л. ед. отр.", 1660),
    ("pot_perf_2sg_neg", "potentiala perfekta 2.yks. kieltävä", "потенциал перфект 2л. ед. отр.", 1670),
    ("pot_perf_3sg_neg", "potentiala perfekta 3.yks. kieltävä", "потенциал перфект 3л. ед. отр.", 1680),
    ("pot_perf_1pl_neg", "potentiala perfekta 1.mon. kieltävä", "потенциал перфект 1л. мн. отр.", 1690),
    ("pot_perf_2pl_neg", "potentiala perfekta 2.mon. kieltävä", "потенциал перфект 2л. мн. отр.", 1700),
    ("pot_perf_3pl_neg", "potentiala perfekta 3.mon. kieltävä", "потенциал перфект 3л. мн. отр.", 1710),
]
