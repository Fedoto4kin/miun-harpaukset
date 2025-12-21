from rest_framework import serializers
from lexicon.models import Definition, Pos, Word


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ["lang", "definition"]


class WordAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "word"]


class WordPreviewSerializer(serializers.ModelSerializer):
    definition = DefinitionSerializer(many=True, source="definition_set")
    pos = serializers.CharField(source="pos.abbr", read_only=True)
    pos_name_ru = serializers.CharField(source="pos.name_ru", read_only=True)
    pos_name_fi = serializers.CharField(source="pos.name_fi", read_only=True)
    speech = serializers.SerializerMethodField()
    alias_words = WordAliasSerializer(many=True, source="alias")

    class Meta:
        model = Word
        fields = [
            "id",
            "word",
            "pos",
            "pos_name_ru",
            "pos_name_fi",
            "definition",
            "speech",
            "alias_words",
            "variant",
            "additional",
        ]

    def get_speech(self, obj):
        request = self.context.get("request")
        if obj.speech and obj.speech.media:
            return request.build_absolute_uri(obj.speech.media.url)
        return None


class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pos
        fields = ["id", "abbr", "name_ru", "name_fi"]