from rest_framework import serializers

from grammar.models import GrammarTable
from lessons.models import Exercise, Lesson, Module, Tag
from lexicon.models import Base, Definition, Pos, Word


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = [
            "id",
            "base",
        ]


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


class LessonSerializer(serializers.ModelSerializer):
    speech = serializers.FileField(source="speech.media", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "full_name",
            "number",
            "title",
            "description",
            "is_enabled",
            "slogan",
            "speech",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "code", "name", "hint_russian", "hint_finnish"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "exercise_type", "data", "has_answers_check"]


class ModuleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    speech = serializers.FileField(source="speech.media", read_only=True, use_url=True)
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            "id",
            "lesson",
            "html_content",
            "number",
            "tags",
            "speech",
            "exercises",
        ]


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
