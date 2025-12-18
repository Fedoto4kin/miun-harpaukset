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

    def construct_data(self, command):
        """
        Constructor for 'Fill in the blank' exercises.
        """
        data = []
        command.stdout.write("Создание упражнения 'Fill in the Blank'.")
        order_counter = 10  # Start from 10

        while True:
            # Prompt for the text of the exercise
            text = input(
                "Введите текст задания (или 's' для пропуска, 'q' для завершения): "
            )
            if text.lower() == "q":
                break
            elif text.lower() == "s":
                text = None  # Skip the text field

            # Prompt for questions
            questions = []
            while True:
                question = input(
                    "Введите вопрос (или 'n' для следующего блока, 's' для показа JSON, 'q' для завершения): "
                )
                if question.lower() == "q":
                    break
                elif question.lower() == "n":
                    break  # Move to the next block
                elif question.lower() == "s":
                    # Show the current JSON
                    current_data = data.copy()
                    if text is not None:
                        current_block = {"order": order_counter, "questions": questions}
                        if text is not None:
                            current_block["text"] = text
                        current_data.append(current_block)
                    command.stdout.write("Текущий JSON:")
                    command.stdout.write(
                        json.dumps(current_data, indent=4, ensure_ascii=False)
                    )
                    continue
                questions.append({"question": question})

            # Create the exercise block
            exercise_block = {"order": order_counter, "questions": questions}
            if text is not None:
                exercise_block["text"] = text

            data.append(exercise_block)

            # Increment the order counter by 10
            order_counter += 10

            # If the user entered 'n', continue to the next block
            if question.lower() == "n":
                continue
            # If the user entered 'q', finish
            elif question.lower() == "q":
                break

        return data
