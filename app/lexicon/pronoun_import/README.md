# pronoun_import — готовые парадигмы местоимений

Источник: `Mestoimenia.docx` (таблица личных и указательных).
Данные вшиты в `data.py` (не runtime).

```bash
python manage.py test lexicon.tests.test_pronoun_import
python manage.py import_pronouns [--dry-run]
```

Аккузатив (`acc_sg` / `acc_pl`) создаётся при импорте, если ещё нет в БД.
Остальные падежи — существующие `GrammarForm` noun (`nom_sg` …).
