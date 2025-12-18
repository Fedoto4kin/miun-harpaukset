from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


class ReverseSearchSuggestionsView(APIView):
    def get(self, request, *args, **kwargs):
        search = request.query_params.get("query", "").lower()
        if len(search) >= 2:
            suggestions = (
                Definition.objects.filter(definition_lcase__icontains=search)
                .values("definition")
                .annotate(count=Count("definition"))
                .order_by("definition")[:10]
            )

            suggestions_list = [
                {
                    "word": _["definition"],
                }
                for _ in suggestions
            ]
            return Response(suggestions_list)
        return Response([])
