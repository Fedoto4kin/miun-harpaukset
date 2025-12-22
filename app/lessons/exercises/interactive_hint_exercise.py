from .contracts import ExerciseSchema


class InteractiveHintExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Schema for interactive hints in the text.
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
                            "hint_button": {"type": "boolean", "default": True},
                        },
                        "required": ["text", "answer"],
                    },
                    "minItems": 1,
                }
            },
            "required": ["questions"],
        }

    def fill_default(self):
        """
        Returns the default data for the 'Interactive Hints' exercise.
        """
        return {
            "questions": [
                {
                    "text": "Kakši čikos't'a reunakkeh eletäh, toine toista ei nähä.",
                    "answer": "šilmät",
                    "hint_button": True,
                }
            ]
        }
