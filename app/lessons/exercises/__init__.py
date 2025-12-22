# exercises/__init__.py
from .fill_blank_exercise import FillBlankExercise
from .fill_blank_table_exercise import FillBlankTableExercise
from .fill_blank_text_exercise import FillBlankTextExercise
from .fill_gap_with_choice_exercise import FillGapWithChoiceExercise
from .fill_word_exercise import FillWordExercise
from .interactive_hint_exercise import InteractiveHintExercise
from .match_pair_exercise import MatchPairExercise
from .match_pair_multiple_exercise import MatchPairMultipleExercise
from .match_pair_slots_exercise import MatchPairSlotsExercise
from .sentence_assembly_prefilled_exercise import SentenceAssemblyPrefilledExercise
from .sentence_assembly_simple_exercise import SentenceAssemblySimpleExercise
from .syllable_assembly_exercise import SyllableAssemblyExercise

__all__ = [
    'ExerciseSchema',
    'FillBlankExercise',
    'FillBlankTableExercise',
    'FillBlankTextExercise',
    'FillGapWithChoiceExercise',
    'FillWordExercise',
    'InteractiveHintExercise',
    'MatchPairExercise',
    'MatchPairMultipleExercise',
    'MatchPairSlotsExercise',
    'SentenceAssemblyPrefilledExercise',
    'SentenceAssemblySimpleExercise',
    'SyllableAssemblyExercise',
]