from .base_exercise import ExerciseSchema


class InteractiveHintExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для интерактивных подсказок в тексте.

        Example data:
        {
            "questions": [
                {
                    "text": "Kakši čikosʼtʼa reunakkeh eletäh, toine toista ei nähä.",
                    "answer": "šilmät",
                    "hint_button": true
                },
                {
                    "text": "Keššellä kandone, kahen puolen neidozet, kočitah, kočitah, yhteh ei šuaha.",
                    "answer": "nenä da šilmät",
                    "hint_button": true
                }
            ]
        }
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
                            "text": {"type": "string"},
                            "answer": {"type": "string"},
                            "hint_button": {"type": "boolean", "default": true},
                        },
                        "required": ["text", "answer"],
                    },
                    "minItems": 1,
                }
            },
            "required": ["questions"],
        }
