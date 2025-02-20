from .base_exercise import ExerciseSchema

class FillBlankTableExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Fill in the blank table'.

        Example data for FillBlankTable schema:

        {
            "rows": 18,
            "cols": 2,
            "class": "table-borderless",
            "table": [
                [
                    {
                        "class": ["table-warning", "fw-bold"],
                        "content": "Yks. nom."
                    },
                    {
                        "class": ["table-warning", "fw-bold"],
                        "content": "Mon. nom."
                    }
                ],
                [
                    {
                        "class": ["table-warning", "fw-bold"],
                        "content": "lämmin alane"
                    },
                    {
                        "content": "{lämbimät alazet}"
                    }
                ],
                ...
                [
                    {
                        "class": ["table-warning", "fw-bold"],
                        "content": "pahuš"
                    },
                    {
                        "content": "[10*:pahukšet]"
                    }
                ]
            ]
        }

        Explanation of the "table" format:
        - "rows": number of rows in the table.
        - "cols": number of columns in the table.
        - "class": (optional) CSS classes for the table.
        - "table": represents the content of the table as an array of rows, where each row is an array of cells.
        - Each cell is an object with the following properties:
            - "class": (optional) an array of CSS classes for the cell.
            - "content": the content of the cell, which may include patterns like [n*:ANSWERS] or {TEXT}.
        - The patterns used in the "content":
            - [n*:ANSWERS] is used to indicate fill-in-the-blank content, where:
              - n* - represents the placeholder for the missing part.
              - ANSWERS - possible answers separated by the '|' symbol.
            - {TEXT} is used to indicate span content where:
              - TEXT - represents text that will be displayed inside a span element with a specific class.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "rows": {
                    "type": "integer",
                    "description": "Number of rows in the table"
                },
                "cols": {
                    "type": "integer",
                    "description": "Number of columns in the table"
                },
                "class": {
                    "type": "string",
                    "description": "CSS classes for the table"
                },
                "table": {
                    "type": "array",
                    "description": "Array of rows in the table",
                    "items": {
                        "type": "array",
                        "description": "Array of cells in a row",
                        "items": {
                            "type": "object",
                            "properties": {
                                "class": {
                                    "type": "array",
                                    "description": "CSS classes for the cell",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Content of the cell, may include fill-in-the-blank patterns"
                                }
                            },
                            "required": ["content"]
                        }
                    }
                }
            },
            "required": ["rows", "cols", "table"]
        }
