"""Ярлыки при омонимии слотов одной орфографии."""


def collect_grammar_labels(wordforms) -> list[str]:
    """Уникальные name_krl в порядке слотов (без склейки — в UI по строкам)."""
    labels = []
    seen = set()
    for wf in wordforms:
        lab = wf.grammar_form.name_krl
        if lab not in seen:
            seen.add(lab)
            labels.append(lab)
    return labels
