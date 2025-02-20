import os
import json
from django.core.management.base import BaseCommand
from lessons.exercises import (
    FillBlankExercise,
    FillBlankTableExercise,
    FillBlankTextExercise,
    FillGapWithChoiceExercise,
    FillWordExercise,
    MatchPairExercise,
    SentenceAssemblyPrefilledExercise,
    SentenceAssemblySimpleExercise,
    SyllableAssemblyExercise,
)
from lessons.models.exercise import ExerciseType  # Import ExerciseType from your models/exercise.py file

# Dictionary to map exercise types to their corresponding classes
EXERCISE_CLASSES = {
    ExerciseType.FILL_BLANK.value: FillBlankExercise,
    ExerciseType.FILL_BLANK_TABLE.value: FillBlankTableExercise,
    ExerciseType.SYLLABLE_ASSEMBLY.value: SyllableAssemblyExercise,
    ExerciseType.FILL_BLANK_TEXT.value: FillBlankTextExercise,
    ExerciseType.SENTENCE_ASSEMBLY.value: SentenceAssemblySimpleExercise,
    ExerciseType.SENTENCE_ASSEMBLY_WITH_PREFILL.value: SentenceAssemblyPrefilledExercise,
    ExerciseType.MATCH_PAIR.value: MatchPairExercise,
    ExerciseType.MATCH_PAIR_SLOTS.value: MatchPairExercise,  # Use the same class if the logic matches
    ExerciseType.FILL_GAP_WITH_CHOICE.value: FillGapWithChoiceExercise,
    ExerciseType.FILL_WORD.value: FillWordExercise,
}

class Command(BaseCommand):
    help = "JSON constructor for creating exercises."

    def clear_screen(self):
        """Clear the terminal screen."""
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For Unix-like systems (Linux, macOS)
            os.system('clear')

    def handle(self, *args, **kwargs):
        while True:  # Main loop to allow returning to exercise selection
            # Display available exercises
            self.stdout.write("Доступные упражнения:")
            for i, (exercise_value, exercise_label) in enumerate(ExerciseType.choices(), start=1):
                self.stdout.write(f"{i}. {exercise_label} ({exercise_value})")
            self.stdout.write("Введите 'q' для выхода.")

            # Prompt the user to select an exercise
            exercise_choice = input("Введите номер упражнения: ")
            if exercise_choice.lower() == 'q':  # Exit if the user enters 'q'
                self.stdout.write("Выход из конструктора.")
                break

            try:
                exercise_choice = int(exercise_choice)
                if exercise_choice < 1 or exercise_choice > len(ExerciseType):
                    raise ValueError
            except ValueError:
                self.stdout.write(self.style.ERROR("Неверный выбор. Пожалуйста, введите число из списка."))
                continue  # Return to exercise selection

            # Get the selected exercise
            exercise_value = ExerciseType.choices()[exercise_choice - 1][0]  # Get the value from the tuple
            exercise_class = EXERCISE_CLASSES.get(exercise_value)

            if not exercise_class:
                self.stdout.write(self.style.ERROR("Ошибка: Упражнение не найдено."))
                continue  # Return to exercise selection

            # Clear the screen after selecting an exercise
            self.clear_screen()

            # Create an instance of the exercise
            exercise = exercise_class()

            # Display the schema description and example data
            self.stdout.write(f"\nВы выбрали упражнение: {ExerciseType.choices()[exercise_choice - 1][1]}")  # Use the label
            self.stdout.write("Описание схемы:")
            self.stdout.write(exercise.schema.get("description", "Описание отсутствует."))
            self.stdout.write("\nПример данных:")
            self.stdout.write(json.dumps(exercise.schema.get("examples", {}), indent=4, ensure_ascii=False))

            # Use the constructor to create data
            data = exercise.construct_data(self)  # Pass the command object
            if data is None:
                self.stdout.write(self.style.ERROR("Конструктор для этого упражнения не реализован."))
                continue  # Return to exercise selection

            # Validate the data and display the result
            try:
                exercise.validate(data)
                self.stdout.write(self.style.SUCCESS("Данные успешно валидированы!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка валидации: {e}"))

            # Display the result and exit
            self.stdout.write("Результат:")
            self.stdout.write(json.dumps(data, indent=4, ensure_ascii=False))
            break  
