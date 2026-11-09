from django.db.models import Exists, OuterRef, Prefetch, Q
from rest_framework import generics

from api_v0.serializers import WordPreviewSerializer
from lexicon.models import KRL_ABC, Word, WordForm


class SearchViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):
        search = self.request.query_params.get("query", "").lower()
        prepared = Word.search_prepare(string=search) if search else ""
        if not prepared:
            return Word.objects.none()

        matched_forms_qs = WordForm.objects.filter(
            form_clean__istartswith=prepared
        ).select_related("grammar_form")

        queryset = (
            Word.objects.filter(
                Q(word_clean__istartswith=prepared)
                | Q(wordform_set__form_clean__istartswith=prepared)
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

            lemma_hit = q.word_clean.lower().startswith(prepared)
            matched = getattr(q, "matched_wordforms", None) or []
            if not lemma_hit and matched:
                wf = matched[0]
                q._matched_form = wf.form
                q._matched_form_label_krl = wf.grammar_form.name_krl
            else:
                q._matched_form = None
                q._matched_form_label_krl = None

        return sorted(
            results,
            key=lambda word: [KRL_ABC.lower().index(c) for c in word.krl_slugify()],
        )
