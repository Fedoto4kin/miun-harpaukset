from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lessons.models import Module

class ModuleContentView(APIView):
    def get(self, request, module_id):
        try:
            module = Module.objects.get(id=module_id)
            return Response({'html_content': module.html_content}, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
        