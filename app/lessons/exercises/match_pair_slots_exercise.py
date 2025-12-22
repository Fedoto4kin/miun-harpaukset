from .contracts.base_exercise import ExerciseSchema
from .match_pair_exercise import MatchPairExercise


class MatchPairSlotsExercise(ExerciseSchema):
    """
    Специальный класс для упражнения 'Match the Pair with slots for sentences'
    Может использовать ту же схему, что и MatchPairExercise, но с другим fill_default
    """
    @property
    def schema(self):
        # Можно использовать ту же схему, что и MatchPairExercise
        return MatchPairExercise().schema
    
    def fill_default(self):
        """
        Returns the default data for 'Match the Pair with slots for sentences'
        """
        return {
            "questions": [
                {
                    "pairs": [
                        {"pair": "paha", "word": "hyvä"},
                        {"pair": "levie", "word": "kaida"},
                    ]
                }
            ]
        }