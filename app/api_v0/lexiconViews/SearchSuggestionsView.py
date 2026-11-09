from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from lexicon.models import Word, WordForm


class SearchSuggestionsView(APIView):

    def get(self, request, *args, **kwargs):
        search = request.query_params.get("query", "").lower()
        if len(search) >= 2:
            prepared = Word.search_prepare(string=search)
            suggestions = (
                Word.objects.filter(
                    Q(word_clean__istartswith=prepared)
                    | Q(pk__in=WordForm.objects.for_search(prepared).values("word_id"))
                )
                .select_related("pos")
                .distinct()[:10]
            )
            suggestions_list = [
                {
                    "word": _.word.replace("|", ""),
                    "word_id": _.id,
                    "pos": _.pos.abbr,
                    "variant": _.variant,
                    "additional": _.additional,
                }
                for _ in suggestions
            ]
            return Response(suggestions_list)
        return Response([])
