from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lessons.models import Module

from api_v0.serializers import ModuleSerializer


class ModuleContentView(APIView):

    def get(self, request, module_id):
        try:
            module = Module.objects.get(id=module_id)
            serializer = ModuleSerializer(module, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response(
                {"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get_serializer_class(self):
        return ModuleSerializer

    def get_queryset(self):
        return Module.objects.all()
