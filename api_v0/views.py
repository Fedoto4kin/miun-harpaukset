from rest_framework import viewsets, filters, generics
from .serializers import *


class SearchViewList(generics.ListAPIView):

    def get_serializer_class(self):
        return BaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        search = self.kwargs['search']
        #TODO: group by base, order base_num 
        queryset =  Base.objects.filter(base_slug__startswith=Base.krl_slugify(Base, string=search))
        # Sorting by karelian abc
        return queryset


class PosViewSet(viewsets.ReadOnlyModelViewSet):

    def get_serializer_class(self):
        return PosSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset =  Pos.objects.all()
        return queryset



class WordViewSet(viewsets.ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return WordPreviewSerializer
        return WordDetailSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset =  Word.objects.all()

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(base_set__in=Base.objects.filter(
                base_slug__startswith=Base.krl_slugify(Base, string=search)
                )
            )
            for q in queryset:
                q.definition_set_by_lang = {}
                for df in q.definition_set.all():
                    if df.lang not in q.definition_set_by_lang:
                        q.definition_set_by_lang[df.lang] =  [df.definition,]
                    else:
                        q.definition_set_by_lang[df.lang].append(df.definition)

            return sorted(queryset, key=lambda word: [Word.get_krl_abc().lower().index(c) for c in Base.krl_slugify(Base, word.word)])
        else:
            return ()

        