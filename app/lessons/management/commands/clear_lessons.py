from django.core.management.base import BaseCommand
from django.db import transaction

from lessons.models import (
    Exercise,
    GrammarComment,
    Lesson,
    LessonSpeech,
    Module,
    Tag,
)


class Command(BaseCommand):
    help = (
        "Удаляет все данные приложения lessons "
        "(уроки, модули, упражнения, аудио, теги, грамматические комментарии). "
        "Словарь и grammar не трогает."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Не спрашивать подтверждение",
        )

    def handle(self, *args, **options):
        if not options["no_input"]:
            confirm = input(
                "Удалить ВСЕ данные lessons из локальной БД? [y/N]: "
            ).strip()
            if confirm.lower() not in ("y", "yes"):
                self.stdout.write(self.style.WARNING("Отменено."))
                return

        with transaction.atomic():
            counts = {
                "Exercise": Exercise.objects.all().delete()[0],
                "GrammarComment": GrammarComment.objects.all().delete()[0],
                "LessonSpeech": LessonSpeech.objects.all().delete()[0],
                "Module": Module.objects.all().delete()[0],
                "Tag": Tag.objects.all().delete()[0],
                "Lesson": Lesson.objects.all().delete()[0],
            }

        for name, count in counts.items():
            self.stdout.write(f"  {name}: удалено {count}")

        self.stdout.write(self.style.SUCCESS("Данные lessons очищены."))
