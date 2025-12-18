from rest_framework import generics

from grammar.models import GrammarTable

from .serializers import GrammarTableListSerializer, GrammarTableSerializer


class GrammarTableView(generics.ListAPIView):
    """
    API для получения списка грамматических таблиц
    Только опубликованные, отсортированные по order
    """

    queryset = GrammarTable.objects.filter(is_published=True).order_by("order")
    serializer_class = GrammarTableListSerializer


class GrammarTableDetailView(generics.RetrieveAPIView):
    queryset = GrammarTable.objects.filter(is_published=True)
    serializer_class = GrammarTableSerializer
    lookup_field = "id"
