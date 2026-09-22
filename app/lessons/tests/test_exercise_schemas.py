from django.test import SimpleTestCase
from jsonschema.exceptions import ValidationError

from lessons.models.exercise import Exercise, ExerciseType


class ExerciseSchemaTests(SimpleTestCase):
    def test_every_exercise_type_has_schema(self):
        for exercise_type in ExerciseType:
            exercise = Exercise(exercise_type=exercise_type.value)
            schema = exercise.get_exercise_schema_instance()
            self.assertIsNotNone(
                schema,
                msg=f"No schema mapped for {exercise_type.value}",
            )

    def test_fill_default_passes_schema_validation(self):
        for exercise_type in ExerciseType:
            exercise = Exercise(exercise_type=exercise_type.value)
            schema = exercise.get_exercise_schema_instance()
            default_data = schema.fill_default()
            try:
                schema.validate(default_data)
            except ValidationError as exc:
                self.fail(
                    f"{exercise_type.value} fill_default() failed schema validation: {exc}"
                )

    def test_unknown_type_has_no_schema(self):
        exercise = Exercise(exercise_type="NotARealType")
        self.assertIsNone(exercise.get_exercise_schema_instance())
        self.assertEqual(exercise.get_default_data(), {})
