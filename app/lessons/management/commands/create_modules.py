from django.core.management.base import BaseCommand
from lessons.models import Lesson, Module

class Command(BaseCommand):
    help = 'Создает пустые модули для указанного урока в заданном количестве.'

    def add_arguments(self, parser):
        parser.add_argument('lesson_num', type=int, help='Номер урока')
        parser.add_argument('num_modules', type=int, help='Количество модулей для создания')

    def handle(self, *args, **kwargs):
        lesson_num = kwargs['lesson_num']
        num_modules = kwargs['num_modules']

        try:
            lesson = Lesson.objects.get(number=lesson_num)
        except Lesson.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Урок с номером {lesson_num} не найден.'))
            return

        created_count = 0
        for i in range(1, num_modules + 1):
            if not Module.objects.filter(lesson=lesson, number=i).exists():
                Module.objects.create(
                    lesson=lesson,
                    number=i,
                    html_content=''
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Создан модуль {i} для урока {lesson_num}'))
            else:
                self.stdout.write(self.style.WARNING(f'Модуль {i} для урока {lesson_num} уже существует, пропуск...'))

        self.stdout.write(self.style.SUCCESS(f'Успешно создано {created_count} модулей для урока {lesson_num}'))
