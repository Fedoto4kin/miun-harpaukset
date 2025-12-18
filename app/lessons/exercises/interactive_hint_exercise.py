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

    def construct_data(self, command):
        """
        Конструктор для создания данных интерактивных подсказок.
        """
        data = {"questions": []}

        while True:
            command.stdout.write("\n=== Добавление подсказки ===")

            text = input("Введите текст (с [*1:✓] для места вставки ответа): ")
            answer = input("Введите правильный ответ: ")

            hint_button = input("Добавить кнопку подсказки? (y/n, по умолчанию y): ")
            hint_button_bool = hint_button.lower() != "n"

            data["questions"].append(
                {"text": text, "answer": answer, "hint_button": hint_button_bool}
            )

            more = input("Добавить еще подсказку? (y/n): ")
            if more.lower() != "y":
                break

        return data
