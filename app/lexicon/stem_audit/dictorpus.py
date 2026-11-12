"""Слой 2: сравнение key-форм с Dictorpus dialect=47 (фильтр, не gold)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

from lexicon.stem_audit.normalize import form_key

DEFAULT_DIALECT = 47
DEFAULT_LANG = 4  # Karelian Proper
KEY_CODES = ("gen_sg", "part_sg", "ill_sg", "iness_sg", "ades_sg")

# Gramset labels → наши коды (эвристика по англ./рус. атрибутам Dictorpus)
_GRAM_TO_CODE = (
    (re.compile(r"genitive.*sg|генитив.*ед", re.I), "gen_sg"),
    (re.compile(r"partitive.*sg|партитив.*ед", re.I), "part_sg"),
    (re.compile(r"illative.*sg|иллатив.*ед", re.I), "ill_sg"),
    (re.compile(r"inessive.*sg|инессив.*ед", re.I), "iness_sg"),
    (re.compile(r"adessive.*sg|адессив|allative.*sg", re.I), "ades_sg"),
)

_ROW_RE = re.compile(
    r"<tr[^>]*>\s*<td[^>]*>.*?</td>\s*"
    r"<td[^>]*>\s*(?P<form>.*?)\s*</td>\s*"
    r"<td[^>]*>\s*(?P<gram>.*?)\s*</td>",
    re.I | re.S,
)
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(chunk: str) -> str:
    text = unescape(_TAG_RE.sub("", chunk or ""))
    return re.sub(r"\s+", " ", text).strip()


def dictorpus_wordform_url(
    lemma: str,
    *,
    dialect: int = DEFAULT_DIALECT,
    lang: int = DEFAULT_LANG,
    limit: int = 50,
) -> str:
    q = urllib.parse.urlencode(
        {
            "search_dialect": dialect,
            "search_lang": lang,
            "search_lemma": lemma,
            "search_gramset": "",
            "search_pos": "",
            "search_wordform": "",
            "limit_num": limit,
        }
    )
    return f"http://dictorpus.krc.karelia.ru/ru/dict/wordform?{q}"


def parse_dictorpus_html(html: str) -> Dict[str, Set[str]]:
    """code → set of forms from HTML table."""
    by_code: Dict[str, Set[str]] = {}
    for m in _ROW_RE.finditer(html or ""):
        form = _strip_html(m.group("form"))
        gram = _strip_html(m.group("gram"))
        if not form:
            continue
        for rx, code in _GRAM_TO_CODE:
            if rx.search(gram):
                by_code.setdefault(code, set()).add(form)
                break
    return by_code


class DictorpusCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, lemma: str) -> Path:
        safe = re.sub(r"[^\w\-]+", "_", lemma.lower()) or "lemma"
        return self.cache_dir / f"{safe}.html"

    def get(self, lemma: str) -> Optional[str]:
        p = self._path(lemma)
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
        return None

    def put(self, lemma: str, html: str) -> None:
        self._path(lemma).write_text(html, encoding="utf-8")


def fetch_dictorpus_html(
    lemma: str,
    *,
    cache: Optional[DictorpusCache] = None,
    timeout: float = 20.0,
    sleep_s: float = 0.35,
    force: bool = False,
) -> str:
    if cache and not force:
        hit = cache.get(lemma)
        if hit is not None:
            return hit
    url = dictorpus_wordform_url(lemma)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "miun-harpaukset-stem-audit/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Dictorpus fetch failed for {lemma!r}: {exc}") from exc
    if cache:
        cache.put(lemma, html)
    if sleep_s > 0:
        time.sleep(sleep_s)
    return html


def compare_with_dictorpus(
    our: Dict[str, Optional[str]],
    theirs: Dict[str, Set[str]],
    codes: Iterable[str] = KEY_CODES,
) -> Dict[str, Any]:
    """
    our: code → form (одна наша форма).
    theirs: code → set forms.
    """
    mismatches: Dict[str, Any] = {}
    missing_there: List[str] = []
    for code in codes:
        ours = our.get(code)
        if not ours:
            continue
        pool = theirs.get(code) or set()
        if not pool:
            missing_there.append(code)
            continue
        keys = {form_key(x) for x in pool}
        if form_key(ours) not in keys:
            mismatches[code] = {
                "ours": ours,
                "dictorpus": sorted(pool),
            }
    return {
        "mismatches": mismatches,
        "missing_in_dictorpus": missing_there,
        "ok": not mismatches,
    }


def enrich_with_dictorpus(
    rows: List[Dict[str, Any]],
    *,
    cache_dir: Path,
    all_codes: bool = False,
    force_fetch: bool = False,
) -> List[Dict[str, Any]]:
    """Добавляет dictorpus_* поля к structural (или любым) строкам аудита."""
    cache = DictorpusCache(cache_dir)
    codes = KEY_CODES if not all_codes else KEY_CODES
    out: List[Dict[str, Any]] = []
    for row in rows:
        lemma = row.get("lemma_clean") or row.get("lemma") or ""
        lemma = lemma.replace("|", "")
        our = {
            "gen_sg": row.get("gen_sg"),
            "part_sg": row.get("part_sg"),
            "ill_sg": row.get("ill_sg"),
            "iness_sg": row.get("iness_sg"),
            "ades_sg": row.get("ades_sg"),
        }
        try:
            html = fetch_dictorpus_html(
                lemma, cache=cache, force=force_fetch
            )
            theirs = parse_dictorpus_html(html)
            cmp = compare_with_dictorpus(our, theirs, codes=codes)
            row = {
                **row,
                "dictorpus_forms": {k: sorted(v) for k, v in theirs.items()},
                "dictorpus_compare": cmp,
                "needs_book": bool(cmp["mismatches"]),
            }
        except RuntimeError as exc:
            row = {
                **row,
                "dictorpus_error": str(exc),
                "needs_book": True,
            }
        out.append(row)
    return out


def dump_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n
