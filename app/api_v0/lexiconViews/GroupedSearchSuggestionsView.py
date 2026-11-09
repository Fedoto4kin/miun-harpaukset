from collections import OrderedDict

from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView

from lexicon.models import Word, WordForm

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

        matching_forms_qs = WordForm.objects.filter(
            form_clean__istartswith=prepared
        ).select_related("grammar_form")

        lemma_hits = list(
            Word.objects.filter(word_clean__istartswith=prepared)
            .select_related("pos")
            .prefetch_related(Prefetch("wordform_set", queryset=matching_forms_qs))
            .order_by("word_clean", "id")
        )

        form_word_ids = (
            WordForm.objects.filter(form_clean__istartswith=prepared)
            .values_list("word_id", flat=True)
            .distinct()
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
        seen_clean = set()

        def add_word(word: Word, lemma_prefix_hit: bool) -> None:
            lemma = word.word_clean.replace("|", "")
            key = lemma.lower()
            if key in seen_clean or len(suggestions_list) >= self.LIMIT:
                return
            seen_clean.add(key)

            samples, total = self._sample_forms(word, prepared, lemma)
            exact = [s for s in samples if s["form_clean"] == prepared]
            chain_src = None
            if not lemma_prefix_hit:
                if exact:
                    chain_src = exact[0]
                elif total == 1 and samples:
                    chain_src = samples[0]
            if chain_src:
                suggestions_list.append(
                    {
                        "word": lemma,
                        "matched_form": chain_src["form"],
                        "matched_form_label_krl": chain_src["label_krl"],
                    }
                )
                return

            item = {"word": lemma}
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

        def rank(wf: WordForm):
            return (
                priority.get(wf.grammar_form.code, 100),
                len(wf.form_clean),
                wf.form_clean,
            )

        # Уникальные орфографии, лучший слот на орфографию.
        by_orth = {}
        for wf in word.wordform_set.all():
            if not wf.form_clean.startswith(prepared):
                continue
            if wf.form_clean == lemma_clean:
                continue
            prev = by_orth.get(wf.form_clean)
            if prev is None or rank(wf) < rank(prev):
                by_orth[wf.form_clean] = wf

        candidates = list(by_orth.values())
        total = len(candidates)
        if not candidates:
            return [], 0

        # Корзины по следующей букве после префикса.
        buckets = OrderedDict()
        for wf in sorted(candidates, key=rank):
            rest = wf.form_clean[len(prepared) :]
            next_ch = rest[0] if rest else ""
            buckets.setdefault(next_ch, []).append(wf)

        picked = []
        seen = set()
        # 1) По одной форме с каждой следующей буквы (в порядке лучших).
        for _ch, group in buckets.items():
            wf = group[0]
            if wf.form_clean in seen:
                continue
            seen.add(wf.form_clean)
            picked.append(wf)
            if len(picked) >= limit:
                break

        # 2) Добор, если букв-веток меньше лимита.
        if len(picked) < limit:
            for wf in sorted(candidates, key=rank):
                if wf.form_clean in seen:
                    continue
                seen.add(wf.form_clean)
                picked.append(wf)
                if len(picked) >= limit:
                    break

        samples = [
            {
                "form": wf.form,
                "form_clean": wf.form_clean,
                "label_krl": wf.grammar_form.name_krl,
            }
            for wf in picked
        ]
        return samples, total
