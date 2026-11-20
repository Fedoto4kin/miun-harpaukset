from django.db.models import Count
from rest_framework import generics

from api_v0.serializers import WordPreviewSerializer
from lexicon.models import KRL_ABC, Definition, Word
from lexicon.search import normalize_definition_search


class SearchReverseViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):
        search = normalize_definition_search(
            self.request.query_params.get("query", "")
        )
        if not search:
            return Word.objects.none()
        queryset = Word.objects.filter(
            definition_set__in=Definition.objects.filter(
                definition_lcase__istartswith=search
            )
        ).annotate(total=Count("id"))

        if queryset.exists():
            for q in queryset:
                q.definition_set_by_lang = {}
                for df in q.definition_set.all():
                    if df.lang not in q.definition_set_by_lang:
                        q.definition_set_by_lang[df.lang] = [df.definition]
                    else:
                        q.definition_set_by_lang[df.lang].append(df.definition)

            return sorted(
                queryset,
                key=lambda word: [KRL_ABC.lower().index(c) for c in word.krl_slugify()],
            )
        else:
            return Word.objects.none()
