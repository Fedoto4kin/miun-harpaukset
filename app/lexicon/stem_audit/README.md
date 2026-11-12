# Stem audit — сверка основ

Оффлайн-аудит `Stem` / key-форм для `s.`. Не runtime API.

## Слои

| Слой | Что | Команда |
|------|-----|---------|
| 1 | Структурные эвристики (класс `rebo`/`čuppu`, drift Stem vs `build_stems`) | `audit_stems --layer=1` |
| 2 | Сравнение с Dictorpus dialect=47 (фильтр, не gold) | `audit_stems --layer=2` или `--layer=all` |
| 3 | Арбитраж по книге | отчёт `*_book.md` + ручное решение |

POS: `--pos=s.` (default) или `--pos=s.,a.,pron.,v.`.

Приоритет gold: **Grammatika 2020** → учебник *Miun harpaukset* → Dictorpus.

## Примеры

```bash
# только структура → jsonl
python manage.py audit_stems --layer=1 --out /tmp/stems_l1.jsonl

# suspects слоя 1 + Dictorpus (кэш HTML)
python manage.py audit_stems --layer=all \
  --out /tmp/stems_all.jsonl \
  --book-md /tmp/stems_book.md \
  --cache-dir /tmp/dictorpus_cache

# весь список s. против Dictorpus (дольше)
python manage.py audit_stems --layer=2 --full-pos --out /tmp/stems_d47.jsonl
```

## После решения по книге

1. Добавить слот в `_BOOK_STEM_OVERRIDES` (`stem_import/build_stems.py`)
   или поправить `<code>` в статье.
2. Точечно пересобрать:

```bash
python manage.py regen_lemma --word=rebo
```

3. При необходимости — точечный патч `lexicon/fixtures/lexicon.json` (как для `rebo`),
   без полного regenerate всех лемм.

## Прогон 2026-11 (s., слой 1→3)

| Лемма | Сигнал | Решение |
|-------|--------|---------|
| `rebo` | `-v : -bo` → asymmetric | override stem1=`revo` (уже) |
| `čuppu` | `- : -pu` → `čupn` | override stem1=`čupu` → `čupun` |
| `elätti` | `- : -ti` → `elätn` | override stem1=`eläti` → `elätin` |

Dictorpus d47 для этих статей часто повторяет ту же ошибку словаря — книга/тип геминаты важнее.

Дальше: `audit_stems --pos=a.` / `--pos=s.,a.,pron.,v. --layer=1`.
