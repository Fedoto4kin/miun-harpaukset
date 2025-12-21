from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


class GroupedSearchSuggestionsView(APIView):
    def get(self, request, *args, **kwargs):
        search = request.query_params.get("query", "").lower()

        if len(search) >= 2:
            suggestions = (
                Word.objects.filter(
                    word_clean__istartswith=Word.search_prepare(string=search)
                )
                .values("word_clean")
                .annotate(count=Count("word_clean"))
                .order_by("word_clean")[:10]
            )

            suggestions_list = [
                {
                    "word": _["word_clean"].replace("|", ""),
                }
                for _ in suggestions
            ]
            return Response(suggestions_list)
        return Response([])
