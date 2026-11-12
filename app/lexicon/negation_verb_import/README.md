# negation_verb_import — парадигма `ei` (kield. v.)

Готовые формы вспомогательного отрицательного глагола.
Данные вшиты в `data.py` (не runtime). Не генерируется из Stem.

```bash
python manage.py test lexicon.tests.test_negation_verb_import
python manage.py import_negation_verb [--dry-run]
```

Слоты: `ind_pres_*_pos` + `imp_*_pos` (существующие verb GrammarForm).
