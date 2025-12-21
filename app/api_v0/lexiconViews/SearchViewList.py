from rest_framework import generics

from lexicon.models import KRL_ABC

from api_v0.serializers import WordPreviewSerializer
from lexicon.models import Word


class SearchViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):

        queryset = ()

        search = self.request.query_params.get("query", "").lower()
        if search and len(Word.search_prepare(string=search)):
            queryset = Word.objects.filter(
                word_clean__istartswith=Word.search_prepare(string=search)
            )

        if len(queryset):
            for q in queryset:
                q.definition_set_by_lang = {}
                for df in q.definition_set.all():
                    if df.lang not in q.definition_set_by_lang:
                        q.definition_set_by_lang[df.lang] = [
                            df.definition,
                        ]
                    else:
                        q.definition_set_by_lang[df.lang].append(df.definition)

            return sorted(
                queryset,
                key=lambda word: [KRL_ABC.lower().index(c) for c in word.krl_slugify()],
            )
        else:
            return ()
