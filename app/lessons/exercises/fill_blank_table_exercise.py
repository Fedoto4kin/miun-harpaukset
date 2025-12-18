import json

from .base_exercise import ExerciseSchema


class FillBlankTableExercise(ExerciseSchema):
    @property
    def schema(self):
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "description": """
    Schema for 'Fill in the blank' exercises.
    
    Explanation of the "table" format:
    - "rows": number of rows in the table.
    - "cols": number of columns in the table.
    - "class": (optional) CSS classes for the table.
    - "table": represents the content of the table as an array of rows, where each row is an array of cells.
    - Each cell is an object with the following properties:
        - "class": (optional) an array of CSS classes for the cell.
        - "content": the content of the cell, which may include patterns like [n*:ANSWERS{PREFILLED}] or {TEXT}.
    - The patterns used in the "content":
        - Allow html tags
        - [n*:ANSWERS{PREFILLED}] is used to indicate fill-in-the-blank content, where:
            - n* - represents the placeholder for the missing part.
            - ANSWERS - possible answers separated by the '|' symbol.
            - {PREFILLED} - (optional) a prefilled value for the blank.
        - {TEXT} is used to indicate span content where:
            - TEXT - represents text that will be displayed inside a span element with a specific class.
            """,
            "properties": {
                "rows": {
                    "type": "integer",
                    "description": "Number of rows in the table",
                },
                "cols": {
                    "type": "integer",
                    "description": "Number of columns in the table",
                },
                "class": {"type": "string", "description": "CSS classes for the table"},
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
                                    "items": {"type": "string"},
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Content of the cell, may include fill-in-the-blank patterns with optional prefilled values",
                                },
                            },
                            "required": ["content"],
                        },
                    },
                },
            },
            "required": ["rows", "cols", "table"],
            "examples": [
                {
                    "rows": 2,
                    "cols": 2,
                    "class": "table-borderless",
                    "table": [
                        [
                            {
                                "class": ["table-warning", "fw-bold"],
                                "content": "Yks. nom.",
                            },
                            {
                                "class": ["table-warning", "fw-bold"],
                                "content": "Mon. nom.",
                            },
                        ],
                        [
                            {
                                "class": ["table-warning", "fw-bold"],
                                "content": "lämmin alane",
                            },
                            {"content": "{lämbimät alazet}"},
                        ],
                    ],
                },
                {
                    "rows": 1,
                    "cols": 1,
                    "class": "table-borderless",
                    "table": [[{"content": "Kazi [4*:on{olen}] pertissä."}]],
                },
            ],
        }

    def construct_data(self, command):
        """
        Step-by-step constructor for creating exercise data.
        """
        data = {}

        # Prompt for the number of rows and columns
        data["rows"] = int(input("Введите количество строк: "))
        data["cols"] = int(input("Введите количество столбцов: "))

        # Prompt for CSS classes for the table (optional)
        table_class = input(
            "Введите CSS-классы для таблицы (через пробел или оставьте пустым): "
        )
        if table_class:
            data["class"] = table_class

        # Create the table
        data["table"] = []
        for row in range(data["rows"]):
            command.stdout.write(f"\nЗаполнение строки {row + 1}:")
            current_row = []
            for col in range(data["cols"]):
                command.stdout.write(f"\nЯчейка [{row + 1}, {col + 1}]:")
                cell = {}
                # Prompt for the cell content
                cell["content"] = input(
                    "Введите содержимое ячейки (например, [1*:ä|ö{ä}]): "
                )
                current_row.append(cell)

                cell_class = input(
                    "Введите CSS-классы для ячейки (через пробел или оставьте пустым): "
                )
                if cell_class:
                    cell["class"] = cell_class.split()

            data["table"].append(current_row)
            command.stdout.write("\nТекущий JSON:")
            command.stdout.write(json.dumps(data, indent=4, ensure_ascii=False))

        return data
