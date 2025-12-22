#!/usr/bin/env python
"""
Одноразовый скрипт для импорта основ из HTML-разметки с использованием BeautifulSoup.
Запуск: python import_stems_bs4.py --html-file dictionary.html
"""

import os
import sys
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

# Добавляем путь к Django проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.krl.settings")

import django

django.setup()

from bs4 import BeautifulSoup

from lexicon.models import Pos, Stem, Word


class StemParserBS4:
    """Парсер HTML с использованием BeautifulSoup"""

    SUPPORTED_POS = ["s.", "a.", "v."]  # Только эти части речи

    @staticmethod
    def parse_html_file(html_file: str) -> List[Dict]:
        """Парсит файл, возвращает только записи с поддерживаемыми частями речи"""
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        entries = []

        for p in soup.find_all("p"):
            b_tag = p.find("b")
            code_tag = p.find("code")
            i_tag = p.find("i")

            if not all([b_tag, code_tag, i_tag]):
                continue

            lemma_with_pipe = b_tag.get_text(strip=True)
            stems_code = code_tag.get_text(strip=True)
            pos_raw = i_tag.get_text(strip=True)

            # Определяем часть речи
            pos_abbr, special_marks = StemParserBS4._parse_pos_and_marks(pos_raw)

            # Пропускаем неподдерживаемые части речи
            if pos_abbr not in StemParserBS4.SUPPORTED_POS:
                continue

            lemma = lemma_with_pipe.replace("|", "")

            entries.append(
                {
                    "lemma": lemma,
                    "lemma_with_pipe": lemma_with_pipe,
                    "pos_abbr": pos_abbr,
                    "special_marks": special_marks,
                    "stems_code": stems_code,
                }
            )

        return entries

    @staticmethod
    def _parse_pos_and_marks(pos_raw: str) -> Tuple[str, List[str]]:
        """Извлекает часть речи и пометы"""
        pos_raw = pos_raw.lower().strip()
        parts = []
        current = ""

        for char in pos_raw:
            if char == ".":
                if current:
                    parts.append(current)
                    current = ""
                parts.append(".")
            elif char == " ":
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char

        if current:
            parts.append(current)

        special_marks = []
        pos_abbr = ""

        i = 0
        while i < len(parts):
            part = parts[i]

            if part in ["s", "a", "v"]:
                pos_abbr = f"{part}."
            elif part == "pl":
                special_marks.append("pl")
            elif part == "sing":
                special_marks.append("sing")
            elif part == "def":
                special_marks.append("v_def")

            i += 1

        return pos_abbr, special_marks


class StemBuilderSimple:
    """Упрощенный строитель основ"""

    @staticmethod
    def create_stems_for_word(word: Word, parsed_data: Dict) -> List[Stem]:
        """Создает основы для слова (упрощенная версия)"""
        lemma = parsed_data["lemma"]
        pos_abbr = parsed_data["pos_abbr"]
        stem_parts = parsed_data["stem_parts"]
        special_marks = parsed_data["special_marks"]

        stems = []

        # Определяем сколько основ нужно создать
        if pos_abbr == "v.":
            stem_count = 8  # 0-7
        else:
            stem_count = 6  # 0-5

        # Создаем основы
        for i in range(stem_count):
            form = StemBuilderSimple._get_stem_form(
                lemma, i, stem_parts, pos_abbr, special_marks
            )
            if form:
                stem = StemBuilderSimple._create_stem(word, i, form, special_marks)
                if stem:
                    stems.append(stem)

        return stems

    @staticmethod
    def _get_stem_form(
        lemma: str,
        stem_number: int,
        stem_parts: List[Dict],
        pos_abbr: str,
        special_marks: List[str],
    ) -> Optional[str]:
        """Получает форму основы по номеру"""

        # Основа 0 всегда лемма
        if stem_number == 0:
            return lemma

        # Определяем какой части шаблона соответствует эта основа
        part_idx = StemBuilderSimple._map_stem_to_part(
            stem_number, pos_abbr, special_marks, len(stem_parts)
        )

        if part_idx is None or part_idx >= len(stem_parts):
            return None

        part = stem_parts[part_idx]

        # Определяем использовать ли чередование
        use_alternant = StemBuilderSimple._should_use_alternant(stem_number, part)

        if use_alternant and part.get("alternant"):
            suffix = part["alternant"]
        else:
            suffix = part["suffix"]

        # Строим полную форму
        return StemBuilderSimple._build_form(lemma, suffix)

    @staticmethod
    def _map_stem_to_part(
        stem_number: int, pos_abbr: str, special_marks: List[str], parts_count: int
    ) -> Optional[int]:
        """Сопоставляет номер основы с частью шаблона"""

        if pos_abbr == "v.":
            # Глаголы
            if "v_def" in special_marks:
                # v.def. - особое сопоставление
                mapping = {1: 0, 3: 1, 4: 2, 5: 3, 6: 4}
            else:
                # Обычные глаголы
                mapping = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 4}
        else:
            # Именные
            if "pl" in special_marks:
                mapping = {4: 0, 5: 0}
            elif "sing" in special_marks:
                mapping = {1: 0, 2: 0, 3: 1}
            elif parts_count == 3:
                mapping = {1: 0, 3: 1, 4: 2}
            else:
                mapping = {1: 0, 2: 0, 3: 1, 4: 2, 5: 2}

        return mapping.get(stem_number)

    @staticmethod
    def _should_use_alternant(stem_number: int, part: Dict) -> bool:
        """Определяет использовать ли чередующуюся форму"""
        if not part.get("has_alternation"):
            return False
        # Для глаголов: основы 2 и 4 используют чередование
        if stem_number in [2, 4]:
            return True
        # Для именных: основы 2 и 5 используют чередование
        if stem_number in [2, 5]:
            return True

        return False

    @staticmethod
    def _build_form(lemma: str, suffix: str) -> str:
        """Строит полную форму основы"""
        if not suffix:
            return lemma

        return lemma + suffix

    @staticmethod
    def _create_stem(
        word: Word, number: int, form: str, special_marks: List[str]
    ) -> Optional[Stem]:
        """Создает объект Stem"""
        stem_type = StemBuilderSimple._get_stem_type(word.pos.abbr, number)
        if not stem_type:
            return None

        special_mark = special_marks[0] if special_marks else ""

        return Stem.objects.create(
            word=word,
            stem_type=stem_type,
            number=number,
            form=form,
            special_mark=special_mark,
        )

    @staticmethod
    def _get_stem_type(pos_abbr: str, number: int) -> Optional[str]:
        """Возвращает тип основы"""
        try:
            if pos_abbr == "v.":
                return getattr(Stem.VerbStemType, f"VERB_{number}")
            elif pos_abbr == "s.":
                return getattr(Stem.NounStemType, f"NOUN_{number}")
            elif pos_abbr == "a.":
                return getattr(Stem.AdjStemType, f"ADJ_{number}")
        except AttributeError:
            return None
        return None


class SimpleStemImporter:
    """Упрощенный импортер"""

    def __init__(
        self,
        html_file: str,
        dry_run: bool = False,
        skip_existing: bool = False,
        limit: int = 0,
    ):
        self.html_file = html_file
        self.dry_run = dry_run
        self.skip_existing = skip_existing
        self.limit = limit
        self.stats = {
            "total_entries": 0,
            "processed": 0,
            "imported": 0,
            "skipped": 0,
            "errors": [],
            "words_not_found": [],
            "pos_mismatches": [],
        }

    def run(self):
        """Запускает импорт"""
        print(f"📄 Чтение файла: {self.html_file}")

        try:
            # Парсим HTML
            entries = StemParserBS4.parse_html_file(self.html_file)
            self.stats["total_entries"] = len(entries)

            if self.limit > 0:
                entries = entries[: self.limit]

            print(f"📋 Найдено записей: {len(entries)}")

            # Обрабатываем записи
            for entry in tqdm(entries, desc="Импорт"):
                self._process_entry(entry)

            self._print_stats()
            return True

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _process_entry(self, entry: Dict):
        """Обрабатывает одну запись для ВСЕХ найденных слов (омонимов)"""
        self.stats["processed"] += 1

        lemma = entry["lemma"]
        lemma_orig = entry["lemma_with_pipe"]
        pos_abbr = entry["pos_abbr"]

        # Ищем ВСЕ слова с данной леммой и частью речи
        words = self._find_words(lemma_orig, pos_abbr)

        if not words:
            # Слово не найдено
            self.stats["words_not_found"].append(f"{lemma_orig} ({pos_abbr})")
            self.stats["skipped"] += 1
            return

        # Логируем если омонимов больше одного
        if len(words) > 1:
            word_ids = sorted([w.id for w in words])

        # Обрабатываем каждое слово
        success_count = 0
        for word in words:
            # Пропускаем если уже есть основы
            if self.skip_existing and word.stems.exists():
                continue

            try:
                if not self.dry_run:
                    # Удаляем старые основы
                    word.stems.all().delete()

                    # Создаем новые основы (для всех омонимов одинаковые)
                    stems = StemBuilderSimple.create_stems_for_word(word, entry)

                    if stems:
                        success_count += 1
                    else:
                        self.stats["errors"].append(
                            f"Не созданы основы: {lemma} (word_id: {word.id})"
                        )
                else:
                    # Dry run - считаем успешным
                    success_count += 1

            except Exception as e:
                self.stats["errors"].append(f"{lemma} (word_id: {word.id}): {str(e)}")

        if success_count > 0:
            self.stats["imported"] += success_count
        else:
            self.stats["skipped"] += 1

    def _find_words(self, lemma: str, pos_abbr: str) -> set:
        """Ищет ВСЕ слова в БД по лемме, части речи и варианту, возвращает set"""
        try:
            pos = Pos.objects.get(abbr=pos_abbr)
            # Заменяем ʼ (U+02BC) на ’ (U+2019)
            db_lemma = lemma.replace("ʼ", "’")

            # Разбираем лемму на слово и вариант
            # Пример: "pi|diä II" → word="pi|diä", variant="II"
            word_part = db_lemma.strip()
            variant_part = None

            # Ищем римскую цифру в конце строки
            import re

            match = re.search(r"\s+([IVXLCDM]+)$", db_lemma)
            if match:
                variant_part = match.group(1)
                word_part = db_lemma[: match.start()].strip()

            # Если нет варианта в лемме, ищем все слова без варианта
            if not variant_part:
                words = Word.objects.filter(
                    word=word_part, pos=pos, variant__isnull=True
                )
            else:
                # Ищем слова с указанным вариантом
                words = Word.objects.filter(
                    word=word_part, pos=pos, variant=variant_part
                )

            return set(words)  # Преобразуем в set для уникальности
        except Pos.DoesNotExist:
            self.stats["errors"].append(f"Часть речи '{pos_abbr}' не найдена в БД")
            return set()

    def _print_stats(self):
        """Выводит статистику"""
        print("\n" + "=" * 60)
        print("📊 СТАТИСТИКА ИМПОРТА")
        print("=" * 60)
        print(f"Всего записей в файле: {self.stats['total_entries']}")
        print(f"Обработано: {self.stats['processed']}")
        print(f"Успешно импортировано: {self.stats['imported']}")
        print(f"Пропущено: {self.stats['skipped']}")

        if self.stats["words_not_found"]:
            print(f"\n⚠️  Слова не найдены в БД ({len(self.stats['words_not_found'])}):")
            for i, word in enumerate(self.stats["words_not_found"][:20]):
                print(f"  {i+1}. {word}")
            if len(self.stats["words_not_found"]) > 20:
                print(f"  ... и еще {len(self.stats['words_not_found']) - 20}")

        if self.stats["errors"]:
            print(f"\n❌ Ошибки ({len(self.stats['errors'])}):")
            for i, error in enumerate(self.stats["errors"][:10]):
                print(f"  {i+1}. {error}")
            if len(self.stats["errors"]) > 10:
                print(f"  ... и еще {len(self.stats['errors']) - 10}")


def main():
    """Точка входа"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Импорт основ из HTML с BeautifulSoup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Примеры:
    %(prog)s --html-file dictionary.html --dry-run      # Тестовый запуск
    %(prog)s --html-file dictionary.html --limit 100    # Первые 100 записей
    %(prog)s --html-file dictionary.html --skip-existing # Пропустить существующие
            """,
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Тестовый запуск без сохранения"
    )
    parser.add_argument(
        "--skip-existing", action="store_true", help="Пропускать слова с основами"
    )
    parser.add_argument(
        "--limit", type=int, default=0, help="Ограничить количество записей"
    )
    parser.add_argument("--output", help="Файл для сохранения логов")

    args = parser.parse_args()
    html_file = "stems.html"

    # Проверяем файл
    if not os.path.exists(html_file):
        print(f"❌ Файл не найден: {html_file}")
        sys.exit(1)

    # Запускаем импорт
    importer = SimpleStemImporter(
        html_file=html_file,
        dry_run=args.dry_run,
        skip_existing=args.skip_existing,
        limit=args.limit,
    )

    print("🚀 Запуск импорта основ...")
    print(f"   Файл: {html_file}")
    print(f"   Dry run: {'Да' if args.dry_run else 'Нет'}")
    print(f"   Пропуск существующих: {'Да' if args.skip_existing else 'Нет'}")
    if args.limit > 0:
        print(f"   Лимит: {args.limit} записей")

    success = importer.run()

    if success:
        print("\n✅ Импорт завершен успешно!")
    else:
        print("\n❌ Импорт завершен с ошибками")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
