from .contracts import ExerciseSchema


class FillGapWithChoiceExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Explanation of the "text" format:
        - The string represents a sentence with a blank that users must fill in.
        - The blank is indicated by the pattern [*n:ANSWERS], where:
            - n - represents the size of the blank (number of characters or width).
            - ANSWERS - correct answer(s) for the blank. Multiple answers are separated by '|'.
        - Example: "Oks’o Smirnova eläy [*4:Kozlovalla]." means the blank is 4 characters wide,
          and the correct answer is "Kozlovalla".
        - For multiple correct answers: "Smirnovat pijetäh [*4:lehmiä|poččie|kanua]." means the blank
          is 4 characters wide, and the correct answers are "lehmiä", "poččie", or "kanua".

        Explanation of the "type" field:
        - "radio": Only one correct answer can be selected.
        - "checkbox": Multiple correct answers can be selected.
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
                            "text": {
                                "type": "string",
                                "pattern": r"\[\*\d+:[^]]+\]",
                                "examples": [
                                    "Oks’o Smirnova eläy [*4:Kozlovalla].",
                                    "Smirnovat pijetäh [*4:lehmiä|poččie|kanua].",
                                ],
                            },
                            "type": {"type": "string", "enum": ["radio", "checkbox"]},
                            "variants": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 1,
                            },
                        },
                        "required": ["text", "type", "variants"],
                    },
                    "minItems": 1,
                }
            },
            "required": ["questions"],
        }

    def fill_default(self):
        """
        Возвращает данные по умолчанию для упражнения 'Fill Gap with Choice'
        """
        return {
            "questions": [
                {
                    "text": "Oks'o Smirnova eläy [*4:Kozlovalla].",
                    "type": "radio",
                    "variants": ["Kozlovalla", "Mikul'n'alla", "Kagrapuussalla"],
                }
            ]
        }
