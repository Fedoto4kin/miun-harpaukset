from rest_framework import serializers

from lessons.models import Exercise, GrammarComment, Lesson, Module, Tag


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


class GrammarCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarComment
        fields = ["id", "html_content", "lang"]
        read_only_fields = ["id"]


class ModuleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    speech = serializers.FileField(source="speech.media", read_only=True, use_url=True)
    exercises = ExerciseSerializer(many=True, read_only=True)
    grammar_comment = GrammarCommentSerializer(read_only=True)

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
            "grammar_comment",
        ]
