from .base_exercise import ExerciseSchema

class FillBlankTextExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Fill in the blank text'.

        Example data for FillBlankText schema:

        {
            "texts": [
                {
                    "text": [
                        "Kazi [4*:on{olen}] pertissä.",
                        ...
                    ]
                }
                ...
            ],
            "example": "Kazi [4*:on] pertissä.",
            "afterWord": "<b>Afterword:</b> Explanation of the text."
        }

        Explanation of the "text" format:
        - The string represents a sentence with missing words that users must fill in.
        - The missing parts are indicated by the pattern [n*:ANSWERS{PREFILLED}], where:
        - n* - represents the placeholder for the missing part.
        - ANSWERS - possible answers separated by the '|' symbol.
        - PREFILLED - (optional) a prefilled value for the blank.
        - Example(optional): "Kazi [4*:on{olen}] pertissä." means that users need to 
          fill in the blank with the correct answer "on" or use the prefilled value "olen".
        - Afterword(optional): Additional information or explanation about the text.
          Shown lower than the text.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "texts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "examples": [
                                        "Kazi [4*:on{olen}] pertissä.",
                                        "Mie [5*:olen{olet}] šuomelane."
                                    ]
                                }
                            }
                        },
                        "required": ["text"]
                    }
                },
                "example": {
                    "type": "string",
                    "examples": [
                        "Example question with [2*:answers{prefilled}]."
                    ]
                },
                "afterWord": {
                    "type": "string",
                    "examples": [
                        "<b>Afterword:</b> Explanation of the text."
                    ]
                }
            },
            "required": ["texts"]
        }
