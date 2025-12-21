from rest_framework import serializers
from grammar.models import GrammarTable


class GrammarTableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarTable
        fields = ["id", "title"]
        read_only_fields = ["id"]


class GrammarTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarTable
        fields = ["id", "title", "html_content", "order", "is_published"]
        read_only_fields = ["id"]
