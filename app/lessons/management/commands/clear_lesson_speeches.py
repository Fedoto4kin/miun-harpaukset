import os
from django.core.management.base import BaseCommand
from django.conf import settings
from lessons.models import LessonSpeech

class Command(BaseCommand):
    help = 'Удаляет файлы записей для уроков, на которые не созданы модели'

    def handle(self, *args, **kwargs):
        media_dir = os.path.join(settings.MEDIA_ROOT, 'lessons')
        if not os.path.exists(media_dir):
            self.stdout.write(self.style.ERROR(f'Директория {media_dir} не существует'))
            return

        files_deleted = 0

        for root, dirs, files in os.walk(media_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if not LessonSpeech.objects.filter(mp3=os.path.relpath(file_path, settings.MEDIA_ROOT)).exists():
                    os.remove(file_path)
                    files_deleted += 1
                    self.stdout.write(self.style.SUCCESS(f'Удален файл: {file_path}'))

        self.stdout.write(self.style.SUCCESS(f'Удалено файлов: {files_deleted}'))
