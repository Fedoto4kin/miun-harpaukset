from .contracts import ExerciseSchema


class SentenceAssemblySimpleExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Sentence Assembly'.

        Example data for SentenceAssembly schema:

        {
            "groups": [
                {
                    "group": 1,
                    "words": [
                        "Mie",
                        "Šie",
                        ...
                    ]
                },
                {
                    "group": 2,
                    "words": [
                        "pagizet",
                        "elän",
                        ...
                    ]
                },
                {
                    "group": 3,
                    "words": [
                        "Tolmačušša.",
                        "karielakši.",
                        ...
                    ]
                }
            ],
            "answers": [
                "Mie|elän|Moskušša.",
                "Mie|elän|Tolmačušša.",
                "Šie|pagizet|karielakši.",
                ...
            ],
            "template": {
                "count": 6,
                "slots": 3
            }
        }

        Explanation of the data format:
        - The "groups" array contains objects representing word groups.
        Each group includes a "group" identifier and an array of "words".
        - The "answers" array contains possible correct sentences that
        can be formed by arranging the given words.
        The | is divider for the words in the sentence by slots.
        - The "template" object defines the structure of the exercise:
        - "count" specifies the number of sentences.
        - "slots" specifies the number of word slots in each sentence.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "groups": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "group": {"type": "integer"},
                            "words": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                },
                                "examples": [
                                    ["Mie", "Šie"],
                                    ["pagizet", "elän"],
                                    ["Tolmačušša", "karielakši"],
                                ],
                            },
                        },
                        "required": ["group", "words"],
                    },
                },
                "answers": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "examples": ["Mie elän Tolmačušša.", "Šie pagizet karielakši."],
                    },
                },
                "template": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "examples": [2]},
                        "slots": {"type": "integer", "examples": [3]},
                    },
                    "required": ["count", "slots"],
                },
            },
            "required": ["groups", "answers", "template"],
        }

    def fill_default(self):
        """
        Возвращает данные по умолчанию для упражнения 'Sentence Assembly'
        """
        return {
            "groups": [
                {
                    "group": 1,
                    "words": ["Mie", "Šie"]
                },
                {
                    "group": 2,
                    "words": ["pagizet", "elän"]
                },
                {
                    "group": 3,
                    "words": ["Tolmačušša.", "karielakši."]
                }
            ],
            "answers": [
                "Mie|elän|Tolmačušša.",
                "Šie|pagizet|karielakši.",
            ],
            "template": {
                "count": 2,
                "slots": 3
            }
        }
