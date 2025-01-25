from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from lessons.models import Module
from ..serializers import ModuleSerializer

class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

    @action(detail=False, methods=['get'], url_path='by-lesson/(?P<lesson_id>\d+)')
    def by_lesson(self, request, lesson_id=None):
        modules = Module.objects.filter(lesson_id=lesson_id)
        serializer = self.get_serializer(modules, many=True)
        
        return Response(serializer.data)
