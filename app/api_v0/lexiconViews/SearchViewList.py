from rest_framework import generics
from ..serializers import *

class SearchViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):

        queryset = ()
        
        search = self.request.query_params.get('query', '').lower()
        if search and len(Word.search_prepare(string=search)):
            queryset = Word.objects.filter(
                word_clean__startswith=Word.search_prepare(string=search)
            )

        if len(queryset):
            for q in queryset:
                q.definition_set_by_lang = {}
                for df in q.definition_set.all():
                    if df.lang not in q.definition_set_by_lang:
                        q.definition_set_by_lang[df.lang] = [df.definition,]
                    else:
                        q.definition_set_by_lang[df.lang].append(df.definition)

            return sorted(
                queryset,
                key=lambda word: [Word.get_krl_abc().lower().index(c) for c in Base.krl_slugify(Base, word.word)]
            )
        else:
            return ()