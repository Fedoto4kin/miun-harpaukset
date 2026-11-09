# stem_import — одноразовый импорт основ

Пакет **не** является частью runtime API/моделей. Нужен, чтобы разово
распарсить `Word.orig` и заполнить `lexicon_stem`.

| Модуль | Назначение |
|--------|------------|
| `parse_orig.py` | HTML `orig` → лемма, шаблон `<code>`, POS, помета |
| `build_stems.py` | шаблон + лемма → словарь `{номер: полная_форма}` |

Запуск импорта в БД: `python manage.py import_stems`.

Тесты (без БД): `python manage.py test lexicon.tests.test_stem_import`.
