from collections import OrderedDict

from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView

from lexicon.models import Word, WordForm
from lexicon.wordform_labels import collect_grammar_labels

# Приоритет «полезных» форм внутри одной ветки следующей буквы.
_NOMINAL_PRIORITY = {
    "gen_sg": 0,
    "part_sg": 1,
    "iness_sg": 2,
    "elat_sg": 3,
    "com_sg": 4,
    "ades_sg": 5,
    "ill_sg": 6,
    "gen_pl": 7,
    "part_pl": 8,
}
_VERB_PRIORITY = {
    "ind_pres_3sg_pos": 0,
    "ind_pres_1sg_pos": 1,
    "ind_impf_3sg_pos": 2,
    "ind_impf_1sg_pos": 3,
    "imp_2sg_pos": 4,
    "inf1": 5,
}

_NOMINAL_SAMPLE = 8
_VERB_SAMPLE = 4
_VERB_MIN_QUERY = 3


class GroupedSearchSuggestionsView(APIView):
    """
    Подсказки по лемме и словоформам.

    Превью форм: по возможности по одной с каждой «следующей буквы»
    после набранного префикса (aka → n/š/l/č…), чтобы ветки парадигмы
    не схлопывались в один алфавитный хвост.
    """

    LIMIT = 10

    def get(self, request, *args, **kwargs):
        search = request.query_params.get("query", "").lower()
        if len(search) < 2:
            return Response([])

        prepared = Word.search_prepare(string=search)
        if not prepared:
            return Response([])

        matching_forms_qs = WordForm.objects.for_search(prepared).select_related(
            "grammar_form"
        )

        lemma_hits = list(
            Word.objects.filter(word_clean__istartswith=prepared)
            .select_related("pos")
            .prefetch_related(Prefetch("wordform_set", queryset=matching_forms_qs))
            .order_by("word_clean", "id")
        )

        form_word_ids = (
            matching_forms_qs.values_list("word_id", flat=True).distinct()
        )
        lemma_ids = {w.id for w in lemma_hits}
        form_only_words = list(
            Word.objects.filter(id__in=form_word_ids)
            .exclude(id__in=lemma_ids)
            .select_related("pos")
            .prefetch_related(Prefetch("wordform_set", queryset=matching_forms_qs))
            .order_by("word_clean", "id")
        )

        suggestions_list = []
        seen_ids = set()

        def add_word(word: Word, lemma_prefix_hit: bool) -> None:
            lemma = word.word_clean.replace("|", "")
            if word.id in seen_ids or len(suggestions_list) >= self.LIMIT:
                return
            seen_ids.add(word.id)

            samples, total = self._sample_forms(word, prepared, lemma)
            exact = [s for s in samples if s["form_clean"] == prepared]
            # Цепочка form→лемма только если префиксу отвечает ровно одна
            # орфография и она точная (akan→akka; akan+akanke → чипы).
            if not lemma_prefix_hit and exact and total == 1:
                chain_src = exact[0]
                needle = chain_src["form_clean"]
                same_orth = [
                    wf
                    for wf in word.wordform_set.all()
                    if any(c == needle for _s, c in wf.search_surfaces())
                ]
                labels = collect_grammar_labels(same_orth) or [
                    chain_src["label_krl"]
                ]
                suggestions_list.append(
                    {
                        "word": lemma,
                        "word_id": word.id,
                        "pos": word.pos.abbr if word.pos_id else "",
                        "matched_form": chain_src["form"],
                        "matched_form_labels_krl": labels,
                    }
                )
                return

            item = {
                "word": lemma,
                "word_id": word.id,
                "pos": word.pos.abbr if word.pos_id else "",
            }
            if samples:
                item["sample_forms"] = [
                    {"form": s["form"], "label_krl": s["label_krl"]} for s in samples
                ]
                if total > len(samples):
                    item["sample_forms_more"] = True
            suggestions_list.append(item)

        for w in lemma_hits:
            add_word(w, lemma_prefix_hit=True)
        for w in form_only_words:
            add_word(w, lemma_prefix_hit=False)

        return Response(suggestions_list)

    def _sample_forms(self, word: Word, prepared: str, lemma: str) -> tuple:
        """
        Возвращает (samples, total_unique).

        Сначала по одной лучшей форме на каждую следующую букву после
        префикса; если лимит не выбран — добираем остальные по приоритету.
        """
        pos = word.pos.abbr if word.pos_id else ""
        if pos == "v." and len(prepared) < _VERB_MIN_QUERY:
            return [], 0

        lemma_clean = Word.search_prepare(lemma)
        priority = _VERB_PRIORITY if pos == "v." else _NOMINAL_PRIORITY
        limit = _VERB_SAMPLE if pos == "v." else _NOMINAL_SAMPLE

        def rank_item(item):
            return (
                priority.get(item["wf"].grammar_form.code, 100),
                len(item["form_clean"]),
                item["form_clean"],
            )

        # Уникальные орфографии (канон + альты), лучший слот на орфографию.
        by_orth = {}
        for wf in word.wordform_set.all():
            for surface, clean in wf.search_surfaces():
                if not clean.startswith(prepared):
                    continue
                if clean == lemma_clean:
                    continue
                if " " in clean and " " not in prepared:
                    continue
                item = {
                    "form": surface,
                    "form_clean": clean,
                    "label_krl": wf.grammar_form.name_krl,
                    "wf": wf,
                }
                prev = by_orth.get(clean)
                if prev is None or rank_item(item) < rank_item(prev):
                    by_orth[clean] = item

        candidates = list(by_orth.values())
        total = len(candidates)
        if not candidates:
            return [], 0

        buckets = OrderedDict()
        for item in sorted(candidates, key=rank_item):
            rest = item["form_clean"][len(prepared) :]
            next_ch = rest[0] if rest else ""
            buckets.setdefault(next_ch, []).append(item)

        picked = []
        seen = set()
        for _ch, group in buckets.items():
            item = group[0]
            if item["form_clean"] in seen:
                continue
            seen.add(item["form_clean"])
            picked.append(item)
            if len(picked) >= limit:
                break

        if len(picked) < limit:
            for item in sorted(candidates, key=rank_item):
                if item["form_clean"] in seen:
                    continue
                seen.add(item["form_clean"])
                picked.append(item)
                if len(picked) >= limit:
                    break

        samples = [
            {
                "form": item["form"],
                "form_clean": item["form_clean"],
                "label_krl": item["label_krl"],
            }
            for item in picked
        ]
        return samples, total
