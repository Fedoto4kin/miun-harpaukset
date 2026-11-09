"""Продуктивные уменьшительные существительных на -ne (Grammatika Novak).

Не runtime: только оффлайн-генерация WordForm на базовой лемме.
Тип склонения как hebone/alane: основы ze / sʼtʼa|sʼtʼä / zi.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .harmony import pick
from .nouns import generate_noun_forms
from .rules_nouns import ALL_NOUN_CODES

# Падежные коды → слоты GrammarForm с префиксом dim_
DIM_PREFIX = "dim_"

# (code, name_krl, name_ru, sort_order) — category=diminutive
_NOUN_LABELS_KRL = {
    "nom_sg": "yksikön nominativa",
    "gen_sg": "yksikön genetiva",
    "part_sg": "yksikön partitiva",
    "ess_sg": "yksikön essiva",
    "transl_sg": "yksikön translativa",
    "iness_sg": "yksikön inessiva",
    "elat_sg": "yksikön elativa",
    "ill_sg": "yksikön illativa",
    "ades_sg": "yksikön adessiva-allativa",
    "ablat_sg": "yksikön ablativa",
    "abess_sg": "yksikön abessiva",
    "com_sg": "yksikön komitativa",
    "prol_sg": "yksikön prolativa",
    "nom_pl": "monikon nominativa",
    "gen_pl": "monikon genetiva",
    "part_pl": "monikon partitiva",
    "ess_pl": "monikon essiva",
    "transl_pl": "monikon translativa",
    "iness_pl": "monikon inessiva",
    "elat_pl": "monikon elativa",
    "ill_pl": "monikon illativa",
    "ades_pl": "monikon adessiva-allativa",
    "ablat_pl": "monikon ablativa",
    "abess_pl": "monikon abessiva",
    "com_pl": "monikon komitativa",
    "prol_pl": "monikon prolativa",
    "instr_pl": "monikon instruktiiva",
}
_NOUN_LABELS_RU = {
    "nom_sg": "номинатив ед.ч.",
    "gen_sg": "генитив ед.ч.",
    "part_sg": "партитив ед.ч.",
    "ess_sg": "эссив ед.ч.",
    "transl_sg": "транслатив ед.ч.",
    "iness_sg": "инессив ед.ч.",
    "elat_sg": "элатив ед.ч.",
    "ill_sg": "иллатив ед.ч.",
    "ades_sg": "адессив-аллатив ед.ч.",
    "ablat_sg": "аблатив ед.ч.",
    "abess_sg": "абессив ед.ч.",
    "com_sg": "комитатив ед.ч.",
    "prol_sg": "пролатив ед.ч.",
    "nom_pl": "номинатив мн.ч.",
    "gen_pl": "генитив мн.ч.",
    "part_pl": "партитив мн.ч.",
    "ess_pl": "эссив мн.ч.",
    "transl_pl": "транслатив мн.ч.",
    "iness_pl": "инессив мн.ч.",
    "elat_pl": "элатив мн.ч.",
    "ill_pl": "иллатив мн.ч.",
    "ades_pl": "адессив-аллатив мн.ч.",
    "ablat_pl": "аблатив мн.ч.",
    "abess_pl": "абессив мн.ч.",
    "com_pl": "комитатив мн.ч.",
    "prol_pl": "пролатив мн.ч.",
    "instr_pl": "инструктив мн.ч.",
}
_NOUN_SORT = {
    "nom_sg": 10,
    "gen_sg": 20,
    "part_sg": 30,
    "ess_sg": 40,
    "transl_sg": 50,
    "iness_sg": 60,
    "elat_sg": 70,
    "ill_sg": 80,
    "ades_sg": 90,
    "ablat_sg": 100,
    "abess_sg": 110,
    "com_sg": 120,
    "prol_sg": 130,
    "nom_pl": 210,
    "gen_pl": 220,
    "part_pl": 230,
    "ess_pl": 240,
    "transl_pl": 250,
    "iness_pl": 260,
    "elat_pl": 270,
    "ill_pl": 280,
    "ades_pl": 290,
    "ablat_pl": 300,
    "abess_pl": 310,
    "com_pl": 320,
    "prol_pl": 330,
    "instr_pl": 340,
}

DIM_FORM_META: Tuple[Tuple[str, str, str, int], ...] = tuple(
    (
        f"{DIM_PREFIX}{code}",
        f"pieniškö · {_NOUN_LABELS_KRL[code]}",
        f"уменьш. {_NOUN_LABELS_RU[code]}",
        1000 + _NOUN_SORT[code],
    )
    for code in ALL_NOUN_CODES
    if code in _NOUN_LABELS_KRL
)


def build_diminutive_stems(nom: str) -> Optional[Dict[int, str]]:
    """
    nom — номинатив базы без '|'.
    Возвращает основы 0..5 для типа -ne или None, если не применимо.
    """
    base = (nom or "").strip()
    if not base:
        return None
    low = base.lower()
    # Уже тип -ne / несклоняемая заготовка
    if low.endswith("ne"):
        return None

    stem0 = base + "ne"
    stem12 = base + "ze"
    stem3 = base + pick(base, "sʼtʼa", "sʼtʼä")
    stem45 = base + "zi"
    return {
        0: stem0,
        1: stem12,
        2: stem12,
        3: stem3,
        4: stem45,
        5: stem45,
    }


def generate_diminutive_forms(nom: str) -> Dict[str, List[str]]:
    """
    Парадигма уменьшительного: ключи без префикса (nom_sg, elat_sg, …).
    """
    stems = build_diminutive_stems(nom)
    if not stems:
        return {}
    return generate_noun_forms(stems)


def dim_code(noun_code: str) -> str:
    return f"{DIM_PREFIX}{noun_code}"
