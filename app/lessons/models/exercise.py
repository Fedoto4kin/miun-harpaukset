from enum import Enum
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ExerciseType(Enum):
    """Types of exercises"""
    INTERACTIVE_HINT = ("InteractiveHint", "Interactive Hints")
    FILL_BLANK = ("FillBlank", "Fill in the Blank Words")
    SYLLABLE_ASSEMBLY = ("SyllableAssembly", "Syllable Assembly")
    FILL_BLANK_TEXT = ("FillBlankText", "Fill in the Blank Text")
    SENTENCE_ASSEMBLY = ("SentenceAssembly", "Sentence Assembly")
    SENTENCE_ASSEMBLY_WITH_PREFILL = (
        "SentenceAssemblyPrefilled",
        "Sentence Assembly with Prefill",
    )
    MATCH_PAIR = ("MatchPair", "Match the Pair")
    MATCH_PAIR_MULTIPLE = ("MatchPairMultiple", "Match the Pair (Multiple)")
    FILL_BLANK_TABLE = ("FillBlankTable", "Fill in the Blank Table")
    MATCH_PAIR_SLOTS = (
        "MatchPairSentenceSlot",
        "Match the Pair with slots for sentantions",
    )
    FILL_GAP_WITH_CHOICE = ("FillGapWithChoice", "Fill Gap with Choice")
    FILL_WORD = ("FillWord", "Fillword Game")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        return [(tag.value, tag.label) for tag in cls]


class Exercise(models.Model):
    module = models.ForeignKey(
        "Module", on_delete=models.CASCADE, related_name="exercises"
    )
    exercise_type = models.CharField(
        max_length=50,
        choices=ExerciseType.choices(),
    )
    data = models.JSONField(encoder=DjangoJSONEncoder, default=dict, blank=True)
    has_answers_check = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Annanda"
        verbose_name_plural = "Annandat"

    def __str__(self):
        return f"{self.get_exercise_type_display()}: {self.module}"

    def get_exercise_schema_instance(self):
        """
        Returns an instance of the schema class for the current exercise type
        """
        from ..exercises import (
            FillBlankExercise,
            FillBlankTableExercise,
            FillBlankTextExercise,
            FillGapWithChoiceExercise,
            FillWordExercise,
            InteractiveHintExercise,
            MatchPairExercise,
            MatchPairMultipleExercise,
            MatchPairSlotsExercise,
            SentenceAssemblyPrefilledExercise,
            SentenceAssemblySimpleExercise,
            SyllableAssemblyExercise,
        )
        # Mapping of exercise types to schema classes
        type_to_schema_class = {
            ExerciseType.FILL_BLANK.value: FillBlankExercise,
            ExerciseType.FILL_BLANK_TABLE.value: FillBlankTableExercise,
            ExerciseType.FILL_BLANK_TEXT.value: FillBlankTextExercise,
            ExerciseType.FILL_GAP_WITH_CHOICE.value: FillGapWithChoiceExercise,
            ExerciseType.FILL_WORD.value: FillWordExercise,
            ExerciseType.INTERACTIVE_HINT.value: InteractiveHintExercise,
            ExerciseType.MATCH_PAIR.value: MatchPairExercise,
            ExerciseType.MATCH_PAIR_MULTIPLE.value: MatchPairMultipleExercise,
            ExerciseType.MATCH_PAIR_SLOTS.value: MatchPairSlotsExercise,
            ExerciseType.SENTENCE_ASSEMBLY_WITH_PREFILL.value: SentenceAssemblyPrefilledExercise,
            ExerciseType.SENTENCE_ASSEMBLY.value: SentenceAssemblySimpleExercise,
            ExerciseType.SYLLABLE_ASSEMBLY.value: SyllableAssemblyExercise,
        }
        
        schema_class = type_to_schema_class.get(self.exercise_type)
        if schema_class:
            return schema_class()
        return None

    def get_default_data(self):
        """
        Returns default data for the current exercise type
        """
        schema_instance = self.get_exercise_schema_instance()
        if schema_instance:
            return schema_instance.fill_default()
        return {}


@receiver(pre_save, sender=Exercise)
def populate_default_exercise_data(sender, instance, **kwargs):
    """
    Signal to populate empty data field with examples from the exercise schema
    """
    # Check if the data field is empty or contains only an empty dict
    if not instance.data or (isinstance(instance.data, dict) and not instance.data):
        default_data = instance.get_default_data()
        if default_data:
            instance.data = default_data