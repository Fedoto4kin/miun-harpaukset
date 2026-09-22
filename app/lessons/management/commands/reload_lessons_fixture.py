import json
import os
import tempfile
from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from lessons.models import Lesson, Module


class Command(BaseCommand):
    help = (
        "Очищает данные lessons и загружает фикстуру. "
        "Числовые content_type у LessonSpeech переписываются "
        "под локальные ContentType (фикстуры с прода без --natural-foreign)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "fixture",
            nargs="?",
            default="lessons/fixtures/lessons.json",
            help="Путь к фикстуре относительно /app (по умолчанию lessons/fixtures/lessons.json)",
        )
        parser.add_argument(
            "--clear-only",
            action="store_true",
            help="Только очистить, не загружать",
        )
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Не спрашивать подтверждение",
        )

    def handle(self, *args, **options):
        fixture = options["fixture"]
        clear_only = options["clear_only"]

        if not clear_only and not os.path.exists(fixture):
            # loaddata ищет относительно INSTALLED_APPS; для проверки —
            # абсолютный путь или путь от cwd (/app в контейнере)
            candidates = [
                fixture,
                os.path.join("/app", fixture),
                os.path.join(
                    os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                    ),
                    "fixtures",
                    "lessons.json",
                ),
            ]
            found = next((p for p in candidates if os.path.isfile(p)), None)
            if not found:
                raise CommandError(
                    f"Файл фикстуры не найден: {fixture}. "
                    "Положите lessons.json в app/lessons/fixtures/ "
                    "(например, через git pull) и повторите."
                )
            fixture_path = found
        else:
            fixture_path = fixture if not clear_only else None

        call_command("clear_lessons", no_input=options["no_input"])

        if clear_only:
            return

        self.stdout.write(f"Подготовка фикстуры: {fixture_path}")
        prepared = self._prepare_fixture(fixture_path)

        try:
            call_command("loaddata", prepared)
        finally:
            if prepared != fixture_path and os.path.isfile(prepared):
                os.remove(prepared)

        self.stdout.write(self.style.SUCCESS("Фикстура lessons загружена."))
        self.stdout.write(
            self.style.NOTICE(
                "Медиа (mp3) фикстура не содержит — файлы нужно скопировать "
                "в media/lessons отдельно, если они нужны локально."
            )
        )

    def _prepare_fixture(self, path):
        with open(path, encoding="utf-8") as fh:
            objects = json.load(fh)

        remapped = self._remap_speech_content_types(objects)
        if remapped == 0:
            return path

        self.stdout.write(
            f"Переписано content_type у LessonSpeech: {remapped} записей "
            "(под локальные ContentType)."
        )

        fd, tmp_path = tempfile.mkstemp(suffix=".json", prefix="lessons_fixture_")
        os.close(fd)
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(objects, fh, ensure_ascii=False, indent=4)
        return tmp_path

    def _remap_speech_content_types(self, objects):
        """
        В dumpdata без --natural-foreign content_type — PK с прода.
        На локали PK ContentType могут отличаться → ломается GFK.
        Определяем, какой CT в фикстуре = Lesson, какой = Module, и
        подставляем локальные PK.
        """
        lesson_ct = ContentType.objects.get_for_model(Lesson).pk
        module_ct = ContentType.objects.get_for_model(Module).pk

        lesson_pks = {o["pk"] for o in objects if o["model"] == "lessons.lesson"}
        module_pks = {o["pk"] for o in objects if o["model"] == "lessons.module"}

        speeches = [o for o in objects if o["model"] == "lessons.lessonspeech"]
        if not speeches:
            return 0

        # Уже natural keys — Django сам разберёт
        sample_ct = speeches[0]["fields"].get("content_type")
        if isinstance(sample_ct, (list, tuple)):
            return 0

        ct_to_oids = defaultdict(set)
        ct_to_codes = defaultdict(list)
        for o in speeches:
            fields = o["fields"]
            ct = fields.get("content_type")
            if ct is None:
                continue
            ct_to_oids[ct].add(fields.get("object_id"))
            ct_to_codes[ct].append(fields.get("code") or "")

        ct_remap = {}
        for ct_id, oids in ct_to_oids.items():
            oids = {oid for oid in oids if oid is not None}
            only_modules = oids - lesson_pks
            only_lessons = oids - module_pks

            if only_modules and not only_lessons:
                ct_remap[ct_id] = module_ct
            elif only_lessons and not only_modules:
                ct_remap[ct_id] = lesson_ct
            else:
                codes = ct_to_codes[ct_id]
                if codes and all(c.endswith(".0") for c in codes if c):
                    ct_remap[ct_id] = lesson_ct
                else:
                    ct_remap[ct_id] = module_ct

            self.stdout.write(
                f"  fixture content_type={ct_id} → local {ct_remap[ct_id]} "
                f"({'lesson' if ct_remap[ct_id] == lesson_ct else 'module'})"
            )

        changed = 0
        for o in speeches:
            fields = o["fields"]
            old = fields.get("content_type")
            if old in ct_remap and ct_remap[old] != old:
                fields["content_type"] = ct_remap[old]
                changed += 1

        return changed
