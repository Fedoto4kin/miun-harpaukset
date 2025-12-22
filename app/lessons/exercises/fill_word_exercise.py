from .contracts import ExerciseSchema

class FillWordExercise(ExerciseSchema):
    @property
    def schema(self):
        """
        Схема для упражнений типа 'Fill Word'.

        Example data for FillWord schema:

        {
            "field": [
                "rdapitčolis",
                "arupzekakvk",
                "pavruuaglaa",
                "ktkohletlut",
                "ušnkielitot",
                "ruänenukame",
                "vuvötättäht",
                "ičaččathami",
                "sutopčimlba",
                "aukriltäišh",
                "tlmateugata"
            ],
            "words": [
                "čolka",
                "kulmat",
                "luomet",
                "viskat",
                "kurvičat",
                "nävöt",
                "tähti",
                "hambahat",
                "tukat",
                "očča",
                "ripčit",
                "šilmät",
                "korvat",
                "nenä",
                "kieli",
                "kagla",
                "leuga",
                "šuu",
                "huulet"
            ],
            "prefilledWords": {
                "čolka": ["1:7", "1:8", "1:9", "2:8", "2:9"],
                "kurvičat": ["4:1", "5:1", "6:1", "7:1", "8:1", "8:2", "8:3", "9:3"]
            }
        }

        Explanation of the data format:
        - The "field" array contains strings representing rows of the letter grid.
        - The "words" array contains the list of words to be found in the grid.
        - The "prefilledWords" object contains pre-filled words as keys and their coordinates as values.
          Coordinates are in the format "x:y", where x is the row number and y is the column number (1-based indexing).
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "field": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "minItems": 1,
                    "examples": ["rdapitčolis", "arupzekakvk", "pavruuaglaa"],
                },
                "words": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "minItems": 1,
                    "examples": ["čolka", "kulmat", "luomet"],
                },
                "prefilledWords": {
                    "type": "object",
                    "patternProperties": {
                        "^.*$": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "pattern": "^\\d+:\\d+$",  # Matches "x:y" format
                            },
                            "minItems": 1,
                        }
                    },
                    "examples": {
                        "čolka": ["1:7", "1:8", "1:9", "2:8", "2:9"],
                        "kurvičat": [
                            "4:1",
                            "5:1",
                            "6:1",
                            "7:1",
                            "8:1",
                            "8:2",
                            "8:3",
                            "9:3",
                        ],
                    },
                },
            },
            "required": ["field", "words"],
        }

    def fill_default(self):
        """
        Возвращает данные по умолчанию для упражнения 'Fillword Game'
        """
        return {
            "field": [
                "rdapitčolis",
                "arupzekakvk",
                "pavruuaglaa",
            ],
            "words": [
                "čolka",
                "kulmat",
                "luomet",
            ],
        }
