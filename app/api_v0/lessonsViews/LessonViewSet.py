from rest_framework import viewsets

from lessons.models import Lesson

from api_v0.serializers import LessonSerializer


class LessonFilter(viewsets.ReadOnlyModelViewSet):
    class Meta:
        model = Lesson


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        return LessonSerializer

    def get_queryset(self):
        queryset = Lesson.objects.all()
        return queryset
