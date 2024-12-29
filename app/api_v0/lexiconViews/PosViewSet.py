from rest_framework import viewsets
from ..serializers import *

class PosViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Pos.objects.all()

    def get_serializer_class(self):
        return PosSerializer

    def get_queryset(self):
        queryset = Pos.objects.all()
        return queryset