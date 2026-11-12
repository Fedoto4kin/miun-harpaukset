from django.db.models import Exists, OuterRef, Prefetch, Q
from rest_framework import generics

from api_v0.serializers import WordPreviewSerializer
from lexicon.compound_split import find_best_compound_split
from lexicon.models import KRL_ABC, Word, WordForm
from lexicon.wordform_labels import collect_grammar_labels


class SearchViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):
        # Алфавитная лента: ?letter=A — префикс по лемме, без словоформ.
        letter = (self.request.query_params.get("letter") or "").strip()
        if letter:
            return self._letter_browse(letter)

        search = self.request.query_params.get("query", "").lower()
        prepared = Word.search_prepare(string=search) if search else ""
        if not prepared:
            return Word.objects.none()

        results = self._exact_hits(prepared)
        if results:
            return results

        # Fallback: слитное сложение → две известные формы.
        split = find_best_compound_split(prepared)
        if not split:
            return []

        parts = [split.left, split.right]
        compound_results = []
        seen = set()
        for part in parts:
            for word in self._exact_hits(part):
                if word.id in seen:
                    continue
                seen.add(word.id)
                word._compound_parts = parts
                word._compound_of = prepared
                compound_results.append(word)
        return compound_results

    def _exact_hits(self, prepared: str):
        """Точная лемма или точная словоформа (/альт); matched_* на объектах."""
        matched_forms_qs = WordForm.objects.for_search(
            prepared, prefix=False
        ).select_related("grammar_form")

        queryset = (
            Word.objects.filter(
                Q(word_clean__iexact=prepared)
                | Q(pk__in=matched_forms_qs.values("word_id"))
            )
            .select_related("pos", "speech")
            .annotate(
                has_paradigm_flag=Exists(
                    WordForm.objects.filter(word_id=OuterRef("pk"))
                )
            )
            .prefetch_related(
                "definition_set",
                "alias",
                Prefetch(
                    "wordform_set",
                    queryset=matched_forms_qs,
                    to_attr="matched_wordforms",
                ),
            )
            .distinct()
        )

        results = list(queryset)
        for q in results:
            q.definition_set_by_lang = {}
            for df in q.definition_set.all():
                q.definition_set_by_lang.setdefault(df.lang, []).append(df.definition)

            lemma_hit = q.word_clean.lower() == prepared
            matched = getattr(q, "matched_wordforms", None) or []
            if not lemma_hit and matched:
                q._matched_form = matched[0].surface_matching(
                    prepared, prefix=False
                )
                q._matched_form_labels_krl = collect_grammar_labels(matched)
            else:
                q._matched_form = None
                q._matched_form_labels_krl = None

        return sorted(
            results,
            key=lambda word: [KRL_ABC.lower().index(c) for c in word.krl_slugify()],
        )

    def _letter_browse(self, letter: str):
        """Все леммы на букву (как раньше через istartswith query=A)."""
        prepared = Word.search_prepare(string=letter)
        if not prepared:
            return Word.objects.none()

        queryset = (
            Word.objects.filter(word_clean__istartswith=prepared)
            .select_related("pos", "speech")
            .annotate(
                has_paradigm_flag=Exists(
                    WordForm.objects.filter(word_id=OuterRef("pk"))
                )
            )
            .prefetch_related("definition_set", "alias")
            .distinct()
        )

        results = list(queryset)
        for q in results:
            q.definition_set_by_lang = {}
            for df in q.definition_set.all():
                q.definition_set_by_lang.setdefault(df.lang, []).append(df.definition)
            q._matched_form = None
            q._matched_form_labels_krl = None

        return sorted(
            results,
            key=lambda word: [KRL_ABC.lower().index(c) for c in word.krl_slugify()],
        )
