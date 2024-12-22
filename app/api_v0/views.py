from rest_framework import viewsets, generics
from .serializers import *
from django.db.models import Count


class SearchViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):
        search = self.kwargs['search']
        if search and len(Word.search_prepare(string=search)):
            queryset = Word.objects.filter(base_set__in=Base.objects.filter(
                base_slug_diacritic__startswith=Word.search_prepare(string=search)
                )
            ).annotate(total=Count('id'))

        if len(queryset):
            for q in queryset:
                q.definition_set_by_lang = {}
                for df in q.definition_set.all():
                    if df.lang not in q.definition_set_by_lang:
                        q.definition_set_by_lang[df.lang] = [df.definition,]
                    else:
                        q.definition_set_by_lang[df.lang].append(df.definition)

            return sorted(queryset, key=lambda word: [Word.get_krl_abc().lower().index(c) for c in Base.krl_slugify(Base, word.word)])
        else:
            return ()


class SearchReverseViewList(generics.ListAPIView):
    pagination_class = None

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get_queryset(self):
        search = self.kwargs['search']
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



class PosViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Pos.objects.all()

    def get_serializer_class(self):
        return PosSerializer

    def get_queryset(self):
        queryset = Pos.objects.all()
        return queryset

