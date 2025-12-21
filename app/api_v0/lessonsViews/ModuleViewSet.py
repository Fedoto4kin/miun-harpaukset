from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from lessons.models import Module

from api_v0.serializers import ModuleSerializer


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

    @action(detail=False, methods=["get"], url_path="by-lesson/(?P<lesson_id>\d+)")
    def by_lesson(self, request, lesson_id=None):
        modules = Module.objects.filter(lesson_id=lesson_id)
        serializer = self.get_serializer(modules, many=True)

        return Response(serializer.data)
