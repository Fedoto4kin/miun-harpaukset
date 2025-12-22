from .contracts import ExerciseSchema


class SentenceAssemblyPrefilledExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Sentence Assembly with Prefilled Data'.

        Example data for SentenceAssembly with Prefilled data schema:

        {
            "groups": [
                {
                    "group": 1,
                    "words": [
                        "buabo<b>n</b> ali diedo<b>n</b>",
                        "poija<b>n</b> ali tyttäre<b>n</b>",
                        ...
                    ]
                },
                {
                    "group": 2,
                    "words": [
                        "muamo.",
                        "velli.",
                        ...
                    ]
                }
            ],
            "answers": [
                "Diedo|on|muamon ali tuaton|tuatto.",
                "Prabuabo|on|buabon ali diedon|muamo.",
                ...
            ],
            "template": {
                "count": 8,
                "slots": 4,
                "examples": [
                    [
                        "Buabo",
                        "on",
                        "muamon ali tuaton",
                        "muamo."
                    ]
                ],
                "prefillers": [
                    [
                        "Diedo",
                        "on",
                        "",
                        ""
                    ],
                    ...
                ]
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
            - "examples" provides sample sentences to illustrate the structure.
            - "prefillers" provides preset words for each sentence slot.
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
                                    [
                                        "buabo<b>n</b> ali diedo<b>n</b>",
                                        "poija<b>n</b> ali tyttäre<b>n</b>",
                                    ],
                                    ["muamo.", "velli."],
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
                        "examples": [
                            "Diedo|on|muamon ali tuaton|tuatto.",
                            "Prabuabo|on|buabon ali diedon|muamo.",
                        ],
                    },
                },
                "template": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "examples": [8]},
                        "slots": {"type": "integer", "examples": [4]},
                        "examples": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "string"},
                                "examples": [
                                    ["Buabo", "on", "muamon ali tuaton", "muamo."]
                                ],
                            },
                        },
                        "prefillers": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "string"},
                                "examples": [
                                    ["Diedo", "on", "", ""],
                                    ["Prabuabo", "on", "", ""],
                                ],
                            },
                        },
                    },
                    "required": ["count", "slots"],
                },
            },
            "required": ["groups", "answers", "template"],
        }

    def fill_default(self):
        """
        Возвращает данные по умолчанию для упражнения 'Sentence Assembly with Prefill'
        """
        return {
            "groups": [
                {
                    "group": 1,
                    "words": [
                        "buabo<b>n</b> ali diedo<b>n</b>",
                        "poija<b>n</b> ali tyttäre<b>n</b>",
                    ]
                },
                {
                    "group": 2,
                    "words": [
                        "muamo.",
                        "velli.",
                    ]
                }
            ],
            "answers": [
                "Diedo|on|muamon ali tuaton|tuatto.",
                "Prabuabo|on|buabon ali diedon|muamo.",
            ],
            "template": {
                "count": 8,
                "slots": 4,
                "examples": [
                    ["Buabo", "on", "muamon ali tuaton", "muamo."]
                ],
                "prefillers": [
                    ["Diedo", "on", "", ""],
                    ["Prabuabo", "on", "", ""],
                ]
            }
        }
