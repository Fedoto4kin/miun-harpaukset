import json

from .base_exercise import ExerciseSchema


class FillBlankExercise(ExerciseSchema):
    @property
    def schema(self):
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "description": """
                Schema for 'Fill in the blank' exercises.
                It may contain more than one block of questions, ordered by order ASC.
                Text of the question block is shown before questions.

                Format of the question string:
                - The string represents a sentence with missing parts that users must fill in.
                - The missing part is indicated by the pattern [**:ANSWERS], where:
                    - ** - represents the length of the missing part.
                    - ANSWERS - possible answers separated by the '|' symbol.
                - Example: "l[**:iä]vä" means that the missing part is 2 characters 
                long and the possible answer is "iä".
            """,
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "order": {"type": "integer"},
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string"},
                                "examples": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                            },
                            "required": ["question"],
                        },
                    },
                },
                "required": ["order", "questions"],
            },
            "examples": [
                {
                    "text": "ua, uo, iä, ie, yö:",
                    "order": 10,
                    "questions": [
                        {"question": "l[**:iä]vä"},
                        {"question": "n[**:uo]ri"},
                        {"question": "m[**:yö]hä"},
                        {"question": "m[**:ua]mo"},
                        {"question": "n[**:ie|ua]gla"},
                    ],
                }
            ],
        }
