from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import *
from django.db.models import Count


class ReverseSearchSuggestionsView(APIView):

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('query', '').lower()
        if len(search) >= 2:
            suggestions = Definition.objects.filter(definition_lcase__icontains=search)[:10]
            suggestions_list = [
                {
                    "word": _.definition,
                    "word_id": _.word.id,
                } for _ in suggestions
            ]
            return Response(suggestions_list)
        return Response([])
