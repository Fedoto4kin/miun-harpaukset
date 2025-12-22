from .contracts import ExerciseSchema


class SyllableAssemblyExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Syllable Assembly'.

        Example data for SyllableAssembly schema:

        {
            "questions": [
                {
                    "word": "omahine",
                    "syllables": [
                        "ne",
                        "o",
                        "hi",
                        "ma"
                    ]
                },
                {
                    "word": "talo",
                    "syllables": [
                        "lo",
                        "ta"
                    ]
                },
                {
                    "word": "šukši",
                    "syllables": [
                        "ši",
                        "šuk"
                    ]
                }
            ]
        }

        Explanation of the "question" format:
        - Each question represents a word and its syllables.
        - "word" is the full word that needs to be assembled.
        - "syllables" is an array of syllables that must
          be arranged in the correct order to form the word.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": {
                                "type": "string",
                            },
                            "syllables": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                },
                            },
                        },
                        "required": ["word", "syllables"],
                    },
                    "examples": [
                        {"word": "omahine", "syllables": ["ne", "o", "hi", "ma"]},
                        {"word": "talo", "syllables": ["lo", "ta"]},
                        {"word": "šukši", "syllables": ["ši", "šuk"]},
                    ],
                }
            },
            "required": ["questions"],
        }

    def fill_default(self):
        """
        Возвращает данные по умолчанию для упражнения 'Syllable Assembly'
        """
        return {
            "questions": [
                {"word": "omahine", "syllables": ["ne", "o", "hi", "ma"]},
                {"word": "talo", "syllables": ["lo", "ta"]},
                {"word": "šukši", "syllables": ["ši", "šuk"]},
            ]
        }
