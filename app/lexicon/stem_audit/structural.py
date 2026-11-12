"""Слой 1: структурные эвристики по Stem / шаблону <code>."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from lexicon.stem_import import build_stems, parse_orig
from lexicon.stem_import.build_stems import parse_template_slots
from lexicon.stem_audit.normalize import form_key, is_vowel, suffix_body

REASON_ASYMM = "asymmetric_gradation"
REASON_EMPTY_WEAK = "empty_weak_consonant_stem"
REASON_SUSPECT_GEN = "suspect_gen_consonant_stem"
REASON_DRIFT = "stem_drift_vs_build"

# Именное склонение (те же слоты 1–3 / gen_sg).
NOMINAL_POS = frozenset({"s.", "a.", "pron."})
AUDITABLE_POS = frozenset({"s.", "a.", "pron.", "v."})


def _stem_map_from_rows(stem_rows: Iterable) -> Dict[int, List[str]]:
    out: Dict[int, List[str]] = {}
    for s in stem_rows:
        if not s.form:
            continue
        out.setdefault(s.number, []).append(s.form)
    return out


def _first(stems: Dict[int, List[str]], number: int) -> Optional[str]:
    forms = stems.get(number) or []
    return forms[0] if forms else None


def check_asymmetric_gradation(code: Optional[str]) -> Optional[str]:
    """
    Слабый суффикс = один согласный, сильный = другой согласный + хвост.
    Пример класса rebo: -v : -bo.
    """
    if not code:
        return None
    slots = parse_template_slots(code)
    if not slots:
        return None
    for weak, strong in slots[0]:
        if not strong:
            continue
        w = suffix_body(weak)
        s = suffix_body(strong)
        if (
            len(w) == 1
            and not is_vowel(w)
            and len(s) > 1
            and not is_vowel(s[0])
            and w.lower() != s[0].lower()
        ):
            return f"{weak} : {strong}"
    return None


def check_empty_weak_consonant_stem(
    code: Optional[str], stem1: Optional[str]
) -> Optional[str]:
    """
    Слабая сторона «-» / пусто, сильная на согласный: `- : -pu` → čup / čupn.
    Флаг только если stem1 реально на согласный (после оверрайда молчим).
    """
    if not code or not stem1 or is_vowel(stem1[-1]):
        return None
    slots = parse_template_slots(code)
    if not slots:
        return None
    for weak, strong in slots[0]:
        if not strong:
            continue
        w = suffix_body(weak)
        s = suffix_body(strong)
        if w == "" and s and not is_vowel(s[0]):
            return f"{weak} : {strong}"
    return None


def check_suspect_gen(stem1: Optional[str], gen_sg: Optional[str]) -> bool:
    """
    Основа 1 на согласный и gen = stem1+'n' → класс revn.
    Нормальные gen на гласный перед n не флажим.
    """
    if not stem1 or not gen_sg:
        return False
    if is_vowel(stem1[-1]):
        return False
    expected = stem1 + "n"
    return form_key(gen_sg) == form_key(expected)


def check_stem_drift(
    lemma: str,
    code: Optional[str],
    pos_abbr: str,
    special_mark: str,
    db_stems: Dict[int, List[str]],
) -> Dict[int, Dict[str, List[str]]]:
    """Слоты, где Stem в БД ≠ build_stems (с учётом book overrides)."""
    built = build_stems(lemma, code, pos_abbr, special_mark)
    drift: Dict[int, Dict[str, List[str]]] = {}
    for number in sorted(set(built) | set(db_stems)):
        if number == 0:
            continue
        a = [form_key(x) for x in (db_stems.get(number) or [])]
        b = [form_key(x) for x in (built.get(number) or [])]
        if a != b:
            drift[number] = {
                "db": list(db_stems.get(number) or []),
                "built": list(built.get(number) or []),
            }
    return drift


def audit_word_structural(word) -> Optional[Dict[str, Any]]:
    """
    Одна лемма. word — lexicon.models.Word с prefetch stems и нужными WordForm.
    """
    pos = word.pos.abbr if word.pos_id else ""
    if pos not in AUDITABLE_POS:
        return None

    parsed = parse_orig(word.orig or "")
    lemma = word.word or parsed.lemma
    code = parsed.code
    mark = next((s.special_mark for s in word.stems.all() if s.special_mark), "") or ""
    if not mark and parsed.special_mark:
        mark = parsed.special_mark

    db_stems = _stem_map_from_rows(word.stems.all())
    stem1 = _first(db_stems, 1)
    stem2 = _first(db_stems, 2)
    stem3 = _first(db_stems, 3)

    gen_sg = None
    iness_sg = None
    ades_sg = None
    for wf in getattr(word, "_audit_forms", None) or []:
        code_f = wf.grammar_form.code
        if code_f == "gen_sg":
            gen_sg = wf.form
        elif code_f == "iness_sg":
            iness_sg = wf.form
        elif code_f == "ades_sg":
            ades_sg = wf.form

    reasons: List[str] = []
    detail: Dict[str, Any] = {}

    asym = check_asymmetric_gradation(code)
    if asym:
        reasons.append(REASON_ASYMM)
        detail["asymmetric_pair"] = asym

    empty = check_empty_weak_consonant_stem(code, stem1)
    if empty:
        reasons.append(REASON_EMPTY_WEAK)
        detail["empty_weak_pair"] = empty

    # gen_sg только у именного склонения
    if pos in NOMINAL_POS and check_suspect_gen(stem1, gen_sg):
        reasons.append(REASON_SUSPECT_GEN)

    drift = check_stem_drift(lemma, code, pos, mark, db_stems)
    if drift:
        reasons.append(REASON_DRIFT)
        detail["drift"] = {str(k): v for k, v in drift.items()}

    if not reasons:
        return None

    return {
        "word_id": word.id,
        "lemma": lemma,
        "lemma_clean": word.word_clean,
        "pos": pos,
        "code": code,
        "special_mark": mark,
        "stem1": stem1,
        "stem2": stem2,
        "stem3": stem3,
        "gen_sg": gen_sg,
        "iness_sg": iness_sg,
        "ades_sg": ades_sg,
        "reasons": reasons,
        "detail": detail,
        "dictorpus_url": (
            "http://dictorpus.krc.karelia.ru/ru/dict/wordform"
            f"?search_dialect=47&search_lang=4&search_lemma={word.word_clean}"
            "&limit_num=50"
        ),
    }


def audit_structural(words: Iterable) -> List[Dict[str, Any]]:
    """Список подозрительных лемм (слой 1)."""
    out: List[Dict[str, Any]] = []
    for word in words:
        row = audit_word_structural(word)
        if row:
            out.append(row)
    return out
