from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lessons.models import Module
from ..serializers import ModuleSerializer 


class ModuleContentView(APIView):
        
    pagination_class = None
    queryset = Module.objects.all()

    def get(self, request, module_id):
        try:
            module = Module.objects.get(id=module_id)
            serializer = ModuleSerializer(module, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        return ModuleSerializer

    def get_queryset(self):
        queryset = Module.objects.all()
        return queryset
