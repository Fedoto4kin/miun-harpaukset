from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lexicon.models import Word
from api_v0.serializers import WordPreviewSerializer


class WordCardView(APIView):

    def get_serializer_class(self):
        return WordPreviewSerializer

    def get(self, request, word_id, *args, **kwargs):
        try:
            word = Word.objects.get(pk=word_id)
        except Word.DoesNotExist:
            return Response(
                {"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = WordPreviewSerializer(word, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
