"""Разрез слитных сложений по словарю (fallback поиска).

Граница в орфографии не размечена: режем там, где обе части — известные
form_clean / word_clean. Exact-хит целого слова обрабатывается снаружи.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Set, Tuple

from lexicon.models import Word, WordForm

MIN_PART_LEN = 3


@dataclass(frozen=True)
class CompoundSplit:
    left: str
    right: str
    score: int


def _candidate_cuts(prepared: str) -> List[Tuple[str, str]]:
    n = len(prepared)
    if n < 2 * MIN_PART_LEN:
        return []
    return [
        (prepared[:i], prepared[i:])
        for i in range(MIN_PART_LEN, n - MIN_PART_LEN + 1)
    ]


def _known_surfaces(parts: Iterable[str]) -> Set[str]:
    parts_list = [p for p in parts if p]
    if not parts_list:
        return set()
    known = set(
        WordForm.objects.filter(form_clean__in=parts_list).values_list(
            "form_clean", flat=True
        )
    )
    known.update(
        Word.objects.filter(word_clean__in=parts_list).values_list(
            "word_clean", flat=True
        )
    )
    return known


def _nom_or_lemma_rights(rights: Sequence[str]) -> Set[str]:
    """Правые члены, которые выглядят как голова сложения (nom / лемма)."""
    if not rights:
        return set()
    heads = set(
        WordForm.objects.filter(
            form_clean__in=rights, grammar_form__code="nom_sg"
        ).values_list("form_clean", flat=True)
    )
    heads.update(
        Word.objects.filter(word_clean__in=rights).values_list(
            "word_clean", flat=True
        )
    )
    return heads


def score_split(
    left: str,
    right: str,
    *,
    head_rights: Set[str],
) -> int:
    score = 0
    if right in head_rights:
        score += 100
    if left.endswith("n"):
        score += 40
    score += len(left) + len(right)
    score += len(right)  # длиннее голова
    return score


def find_compound_splits(prepared: str) -> List[CompoundSplit]:
    """Все валидные разрезы, лучшие первыми."""
    prepared = (prepared or "").strip()
    if not prepared or " " in prepared:
        return []

    cuts = _candidate_cuts(prepared)
    if not cuts:
        return []

    parts: Set[str] = set()
    for left, right in cuts:
        parts.add(left)
        parts.add(right)
    known = _known_surfaces(parts)
    valid = [(left, right) for left, right in cuts if left in known and right in known]
    if not valid:
        return []

    rights = list({right for _, right in valid})
    head_rights = _nom_or_lemma_rights(rights)

    scored = [
        CompoundSplit(
            left=left,
            right=right,
            score=score_split(left, right, head_rights=head_rights),
        )
        for left, right in valid
    ]
    # выше score; при ничьей — длиннее правый (голова), затем длиннее левый
    scored.sort(key=lambda s: (-s.score, -len(s.right), -len(s.left)))
    return scored


def find_best_compound_split(prepared: str) -> Optional[CompoundSplit]:
    splits = find_compound_splits(prepared)
    return splits[0] if splits else None
