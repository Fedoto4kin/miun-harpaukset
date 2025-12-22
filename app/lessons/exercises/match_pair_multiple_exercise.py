from .contracts import ExerciseSchema


class MatchPairMultipleExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Match Pair Multiple'.

        Word - всегда строка (что сопоставляется)
        Pair - может быть строкой ИЛИ массивом строк (варианты правильных ответов)

        Example data for MatchPairMultiple schema:

        {
            "questions": [
                {
                    "pairs": [
                        {
                            "pair": ["nenä", "tukka"],  # ДВА правильных варианта для слова "pitkä"
                            "word": "pitkä"
                        },
                        {
                            "pair": "kiherä",  # Один правильный вариант
                            "word": "piä"
                        },
                        {
                            "pair": ["paha – da oma.", "hyvä – da vieraš"],  # Два варианта
                            "word": "Пример длинного слова"
                        }
                    ]
                }
            ]
        }

        Правила:
        1. Каждое слово (word) имеет один или несколько правильных вариантов (pair)
        2. Пользователь выбирает из общего списка всех возможных пар
        3. Выбранный вариант НЕ исчезает из списка доступных
        4. Можно использовать один вариант для нескольких слов (если он подходит)
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
                            "pairs": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "pair": {
                                            "anyOf": [
                                                {"type": "string"},
                                                {
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                    "minItems": 1,
                                                },
                                            ]
                                        },
                                        "word": {"type": "string"},  # Всегда строка!
                                    },
                                    "required": ["pair", "word"],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["pairs"],
                    },
                }
            },
            "required": ["questions"],
            "additionalProperties": False,
        }

    def fill_default(self):
        """
        Returns the default data for 'Match the Pair (Multiple)'
        """
        return {
            "questions": [
                {
                    "pairs": [
                        {"pair": ["nenä", "tukka"], "word": "pitkä"},
                        {"pair": "kiherä", "word": "piä"},
                    ]
                }
            ]
        }
