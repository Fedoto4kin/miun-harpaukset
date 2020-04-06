from rest_framework import viewsets, filters, generics
from .serializers import *
from django.db.models import Count


class SearchViewList(generics.ListAPIView):

    pagination_class = None

    def get_serializer_class(self):
        return BaseSerializer

    def get_queryset(self):

        search = self.kwargs['search']
        #TODO: group by base, order base_num 
        queryset =  Base.objects.filter(base_slug__startswith=Base.krl_slugify(Base, string=search))
        # Sorting by karelian abc
        return queryset


class SearchReverseViewList(generics.ListAPIView):
    #TODO: add class search by transalate + serializer using word + translate
    pass


class PosViewSet(viewsets.ReadOnlyModelViewSet):

    pagination_class = None

    def get_serializer_class(self):
        return PosSerializer

    def get_queryset(self):

        queryset =  Pos.objects.all()
        return queryset



class WordViewSet(viewsets.ReadOnlyModelViewSet):


    def get_serializer_class(self):
        if self.action == 'list':
            return WordPreviewSerializer
        return WordDetailSerializer

    def get_queryset(self):
        
        queryset = ()
        search = self.request.query_params.get('search', None)
        reverse = self.request.query_params.get('reverse', None) is not None


        if reverse and search:
            queryset = Word.objects.all()
            queryset = Word.objects.filter(
                    definition_set__in=Definition.objects.filter(definition_lcase__search=search.lower())
                    ).annotate(total=Count('id'))
        elif search and len(Base.krl_slugify(Base, string=search)):
            queryset = Word.objects.all()
            queryset = Word.objects.filter(base_set__in=Base.objects.filter(
                base_slug_diacrit__startswith=Base.krl_slugify(Base, string=search)
                )
            )

        if len(queryset):
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
        