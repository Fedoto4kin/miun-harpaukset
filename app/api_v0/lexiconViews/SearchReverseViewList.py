from rest_framework import generics
from ..serializers import *
from django.db.models import Count

class SearchReverseViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):
        search = self.request.query_params.get('query', '').lower()
        queryset = Word.objects.filter(
            definition_set__in=Definition.objects.filter(definition_lcase__istartswith=search.lower())
        ).annotate(total=Count('id'))

        if queryset.exists():
            for q in queryset:
                q.definition_set_by_lang = {}
                for df in q.definition_set.all():
                    if df.lang not in q.definition_set_by_lang:
                        q.definition_set_by_lang[df.lang] = [df.definition]
                    else:
                        q.definition_set_by_lang[df.lang].append(df.definition)

            return sorted(queryset, key=lambda word: [
                Word.get_krl_abc().lower().index(c) for c in Base.krl_slugify(Base, word.word)
            ])
        else:
            return Word.objects.none()