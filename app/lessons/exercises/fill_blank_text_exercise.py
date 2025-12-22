from .contracts import ExerciseSchema


# todo: add title
class FillBlankTextExercise(ExerciseSchema):
    @property
    def schema(self):
        """
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
                                        "Mie [5*:olen{olet}] šuomelane.",
                                    ],
                                },
                            }
                        },
                        "required": ["text"],
                    },
                },
                "example": {
                    "type": "string"
                },
                "afterWord": {
                    "type": "string"
                },
            },
            "required": ["texts"],
        }

    def fill_default(self):
        """
        Returns the default data for 'Fill in the Blank Text'
        """
        return {
            "example": "Example question with [8*:kyžymyš{vaštauš}].",
            "texts": [
                {
                    "text": [
                        "Kazi [4*:on{olen}] pertissä.",
                        "Mie [5*:olen{olet}] šuomelane.",
                    ]
                },
                {
                    "text": [
                        "Myö [8*:pagizemma{paissa}] karielakši."
                    ]
                }
            ],
            "afterWord": "<b>Afterword:</b> Explanation of the text.",
        }
