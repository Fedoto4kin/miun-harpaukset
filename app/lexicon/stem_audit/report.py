"""Отчёты аудита для слоя 3 (арбитраж по книге)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List


def write_book_arbitration_md(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    """
    Markdown-чеклист: книга (Grammatika / учебник) решает mismatch.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows_list: List[Dict[str, Any]] = list(rows)
    lines = [
        "# Stem audit — арбитраж по книге",
        "",
        "Приоритет: Grammatika 2020 → учебник Miun harpaukset → Dictorpus.",
        "После решения: `_BOOK_STEM_OVERRIDES` в `stem_import/build_stems.py`",
        "или правка `<code>` в orig, затем `regen_lemma --word=…`.",
        "",
        f"Подозрительных строк: **{len(rows_list)}**.",
        "",
    ]
    for i, row in enumerate(rows_list, 1):
        lemma = row.get("lemma") or row.get("lemma_clean")
        lines.append(f"## {i}. {lemma} (id={row.get('word_id')})")
        lines.append("")
        lines.append(f"- `<code>`: `{row.get('code')}`")
        lines.append(
            f"- stems: 1=`{row.get('stem1')}` 2=`{row.get('stem2')}` "
            f"3=`{row.get('stem3')}`"
        )
        lines.append(
            f"- forms: gen=`{row.get('gen_sg')}` "
            f"iness=`{row.get('iness_sg')}` ades=`{row.get('ades_sg')}`"
        )
        lines.append(f"- reasons: `{', '.join(row.get('reasons') or [])}`")
        url = row.get("dictorpus_url")
        if url:
            lines.append(f"- Dictorpus: {url}")
        cmp = row.get("dictorpus_compare") or {}
        mm = cmp.get("mismatches") or {}
        if mm:
            lines.append("- Dictorpus mismatches:")
            for code, payload in mm.items():
                lines.append(
                    f"  - `{code}`: ours=`{payload.get('ours')}` "
                    f"dict={payload.get('dictorpus')}"
                )
        if row.get("needs_book"):
            lines.append("- **needs_book**: yes")
        lines.append("- [ ] Решение (книга): _…_")
        lines.append("- [ ] Override / правка orig")
        lines.append(f"- [ ] `regen_lemma --word={row.get('lemma_clean') or ''}`")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return len(rows_list)
