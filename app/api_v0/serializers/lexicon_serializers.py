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
    matched_form = serializers.SerializerMethodField()
    matched_form_labels_krl = serializers.SerializerMethodField()
    has_paradigm = serializers.SerializerMethodField()
    compound_parts = serializers.SerializerMethodField()
    compound_of = serializers.SerializerMethodField()

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
            "matched_form",
            "matched_form_labels_krl",
            "has_paradigm",
            "compound_parts",
            "compound_of",
        ]

    def get_speech(self, obj):
        request = self.context.get("request")
        if obj.speech and obj.speech.media:
            return request.build_absolute_uri(obj.speech.media.url)
        return None

    def get_matched_form(self, obj):
        return getattr(obj, "_matched_form", None)

    def get_matched_form_labels_krl(self, obj):
        return getattr(obj, "_matched_form_labels_krl", None)

    def get_has_paradigm(self, obj):
        if hasattr(obj, "has_paradigm_flag"):
            return bool(obj.has_paradigm_flag)
        if hasattr(obj, "_has_paradigm"):
            return bool(obj._has_paradigm)
        return False

    def get_compound_parts(self, obj):
        parts = getattr(obj, "_compound_parts", None)
        return list(parts) if parts else None

    def get_compound_of(self, obj):
        return getattr(obj, "_compound_of", None)


class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pos
        fields = ["id", "abbr", "name_ru", "name_fi"]
