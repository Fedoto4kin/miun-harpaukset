"""
Готовые парадигмы местоимений из Mestoimenia.docx
(новописьменный тверской собственно карельский).

Столбцы — леммы; строки — падежи (без prol/instr).
Число заложено в лемме: sg vs pl.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

# Несклоняемые по глоссу Novak (нет gen/part; в тексте без парадигмы).
# Пишем только nom_sg = лемма.
INDECLINABLE_LEMMAS: List[str] = [
    "jogo",
    "kudami",
    "molen",
    "moneš",
]

# (lemma, number) — number: "sg" | "pl"
LEMMAS: List[Tuple[str, str]] = [
    ("mie", "sg"),
    ("šie", "sg"),
    ("hiän", "sg"),
    ("myö", "pl"),
    ("työ", "pl"),
    ("hyö", "pl"),
    ("tämä", "sg"),
    ("tua", "sg"),
    ("že", "sg"),
    ("nämä", "pl"),
    ("nua", "pl"),
    ("ne", "pl"),
]

# Сокращение в таблице → база кода GrammarForm (без _sg/_pl)
CASE_LABELS: Dict[str, str] = {
    "ном.": "nom",
    "ген.": "gen",
    "парт.": "part",
    "акк.": "acc",
    "инесс.": "iness",
    "элат.": "elat",
    "илл.": "ill",
    "адесс.": "ades",
    "абл.": "ablat",
    "эсс.": "ess",
    "транс.": "transl",
    "ком.": "com",
    "абесс.": "abess",
}

# case_base → [form per lemma column, same order as LEMMAS]
PARADIGM: Dict[str, List[str]] = {
    "nom": [
        "mie",
        "šie",
        "hiän",
        "myö",
        "työ",
        "hyö",
        "tämä",
        "tua",
        "že",
        "nämä",
        "nua",
        "ne",
    ],
    "gen": [
        "miun",
        "šiun",
        "hänen",
        "miän",
        "tiän",
        "hiän",
        "tämän",
        "tuan",
        "žen",
        "näin",
        "noin",
        "niin",
    ],
    "part": [
        "miut",
        "šiut",
        "hänet",
        "miät",
        "tiät",
        "hiät",
        "tädä",
        "tuada",
        "šidä",
        "näidä",
        "noida",
        "niidä",
    ],
    "acc": [
        "milma",
        "šilma",
        "händä",
        "meidä",
        "teidä",
        "heidä",
        "tämän",
        "tuan",
        "žen",
        "näin",
        "noin",
        "niin",
    ],
    "iness": [
        "miušša",
        "šiušša",
        "häneššä",
        "meissä",
        "teissä",
        "heissä",
        "täššä",
        "tuašša",
        "šissä",
        "näissä",
        "noissa",
        "niissä",
    ],
    "elat": [
        "miušta",
        "šiušta",
        "häneštä",
        "meistä",
        "teistä",
        "heistä",
        "täštä",
        "tuašta",
        "šistä",
        "näistä",
        "noista",
        "niistä",
    ],
    "ill": [
        "miuh",
        "šiuh",
        "häneh",
        "meih",
        "teih",
        "heih",
        "täh",
        "tuah",
        "ših",
        "näih",
        "noih",
        "niih",
    ],
    "ades": [
        "miula",
        "šiula",
        "hänellä",
        "meilä",
        "teilä",
        "heilä",
        "tällä",
        "tuala",
        "šillä",
        "näilä",
        "noila",
        "niillä",
    ],
    "ablat": [
        "miulda",
        "šiulda",
        "häneldä",
        "meildä",
        "teildä",
        "heildä",
        "täldä",
        "tualda",
        "šildä",
        "näildä",
        "noilda",
        "niildä",
    ],
    "ess": [
        "miuna",
        "šiuna",
        "hänenä",
        "meinä",
        "teinä",
        "heinä",
        "tänä",
        "tuana",
        "šinä",
        "näinä",
        "noina",
        "niinä",
    ],
    "transl": [
        "miukši",
        "šiukši",
        "hänekši",
        "meiksi",
        "teiksi",
        "heiksi",
        "täkši",
        "tuakši",
        "šiksi",
        "näiksi",
        "noiksi",
        "niiksi",
    ],
    "com": [
        "miunke",
        "šiunke",
        "hänenke",
        "meinke",
        "teinke",
        "heinke",
        "tämänke",
        "tuanke",
        "ženke",
        "näinke",
        "noinke",
        "niinke",
    ],
    "abess": [
        "miutta",
        "šiutta",
        "hänettä",
        "meittä",
        "teittä",
        "heittä",
        "tättä",
        "tuatta",
        "šittä",
        "näittä",
        "noitta",
        "niittä",
    ],
}


def iter_lemma_forms():
    """Yield (lemma, number, grammar_code, form)."""
    n = len(LEMMAS)
    for case, forms in PARADIGM.items():
        if len(forms) != n:
            raise ValueError(f"PARADIGM[{case}] length {len(forms)} != {n}")
        for (lemma, number), form in zip(LEMMAS, forms):
            yield lemma, number, f"{case}_{number}", form
