from .contracts import ExerciseSchema


class MatchPairExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Schema for 'Match Pair' exercises.

        Explanation of the data format:
        - "title" (optional): Title of the exercise
        - The "questions" array contains objects with "pairs".
        - Each "pair" object includes a "pair" and its corresponding "word".
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "pairs": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "pair": {"type": "string"},
                                        "word": {"type": "string"},
                                    },
                                    "required": ["pair", "word"],
                                },
                                "examples": [
                                    {"pair": "paha", "word": "hyvä"},
                                    {"pair": "levie", "word": "kaida"},
                                ],
                            }
                        },
                        "required": ["pairs"],
                    },
                },
            },
            "required": ["questions"],
        }

    def fill_default(self):
        """
        Returns the default data for 'Match the Pair'
        """
        return {
            "title": "Antonimat",
            "questions": [
                {
                    "pairs": [
                        {"pair": "paha", "word": "hyvä"},
                        {"pair": "levie", "word": "kaida"},
                    ]
                }
            ],
        }
