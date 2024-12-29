from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import *


class SearchSuggestionsView(APIView):

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('query', '').lower()
        if len(search) >= 2:
            suggestions = Word.objects.filter(
                word_clean__startswith=Word.search_prepare(string=search)
            )[:10]
            suggestions_list = [suggestion.word.replace('|', '') for suggestion in suggestions]
            return Response(suggestions_list)
        return Response([])
