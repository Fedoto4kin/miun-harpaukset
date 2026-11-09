# Бэклог — Miun harpaukšet

Собрано из `backlog.md`, TODO в коде и незакрытых заметок в README. Статусы: `open` | `done`.

---

## UX / продукт

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| UX-1 | При скролле страницы урока держать аудиоплеер видимым (sticky/fixed) | `LessonHeaderComponent.vue` | done |
| UX-2 | Выставлять `document.title` с номером модуля при навигации по урокам | `LessonsComponent.vue` | done |

## Контент / упражнения

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| EX-1 | Добавить `title` в схему FillBlankText | `fill_blank_text_exercise.py` | open |

## Лексикон / backend

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| LX-1 | Вынести `Word.search_prepare` в сервисный слой | `lexicon/models/word.py` | open |
| LX-2 | Фильтровать ввод поиска по `KRL_ABC` | `lexicon/models/word.py` | open |

## Морфология — открытые вопросы / расхождения (не блокеры)

Копить здесь по ходу пайплайна; закрывать точечно, не смешивая с текущим POS-этапом.

| ID | Тема | Детали | Статус |
|----|------|--------|--------|
| MORPH-1 | Пустой `orig` / нет основ | `Word` 6140 `hapan` (`a.`), 6141 `ryndäh\|ät` — `orig` пуст, Stem/WordForm = 0. Дозаполнить статьи, потом `import_stems` (+ gen). | open |
| MORPH-2 | Dictorpus `käzi` | dialect=47: `käzilöidä` помечена и как абессив мн., и как партитив мн. У нас абессив `käzittä` / `käzilöittä` — верно; баг разметки ВепКар. | open |
| MORPH-3 | Dictorpus `uni` | комитатив `uniloineh` (-neh) рядом с `-nke`. Grammatika → только `-nke` (`unenke`, `uninke`/`uniloinke`). | open |
| MORPH-4 | pl. tantum `vuattiet` | есть `/`-альты и косвенные мн.; `nom_pl=vuattiet` (лемма) в WordForm не пишется. Решить: всегда класть лемму в nom для `pl`. | open |
| MORPH-5 | `a.` без шаблона основ | `Word` 4179 `kogo` — в `orig` есть `<i>a.</i>`, но нет `<code>…</code>`; Stem/WordForm = 0 (несклоняемое / дефект статьи). | open |
| MORPH-6 | Апостроф мягкости | Канон хранения U+02BC `ʼ`; поиск снимает все варианты (`lexicon.ortho`, `normalize_soft_signs`). Dictorpus/учебник могут давать U+2019 — при сверке нормализовать. | done |
| MORPH-7 | Конд. `zin`/`sin` | Dictorpus иногда даёт пару `…zin`/`…sin` (и `zit`/`sit`); Grammatika — только `z`. Пример: `levittiäčie`. | open |
| MORPH-8 | `pron.` несклоняемые | `jogo`, `kudami`, `molen`, `moneš` — в глоссе Novak без gen/part, в тексте не склоняются. Пишем только `nom_sg`. | done |
| MORPH-9 | `mi`/`nimi` помета `pl.` в orig | В словаре ошибочно `pron. pl.`; глосс Novak ед.ч. Override в `build_stems`; поправить статьи. | open |

Сделано по существительным (`s.`): Stem (+`alt` для `/`), WordForm, поиск, попап; сверка `/`-лемм с dialect=47 — OK кроме MORPH-2…4.

Сделано по прилагательным (`a.`): WordForm через тот же именной генератор (`generate_wordforms --pos=a.`, 243 леммы / 6561 форм; skip: `kogo`, `hapan`); сверка 15 случайных + повтор ERR — OK, кроме MORPH-6 (`palane`).

Сделано по местоимениям (`pron.`): 12 лемм Mestoimenia → WordForm (`import_pronouns`); остальные с `<code>` — именная парадигма (`import_stems` + `generate_wordforms --pos=pron.`; эталон глосс/текст Novak PDF; override `ken`/`niken`). Без шаблона — MORPH-8.

Сделано по глаголам (`v.`): фазы 1–2 — 680 лемм → 77058 WordForm (финитные, потенциал, инф. II–III, причастия, аналитика на 141); схема 73; сверка phase2 (7 лемм) — OK; MORPH-7 (zin/sin) остаётся.

## Документация / DX

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| DX-1 | Описать setup client (dev и prod) в `client/README.md` | `client/README.md` `@todo` | open |
| DX-2 | Указать лицензию в корневом README | `README.md` | open |

## Техдолг (зафиксировано при обзоре, не из TODO)

| ID | Задача | Примечание | Статус |
|----|--------|------------|--------|
| TD-1 | Вынести `SECRET_KEY` / `DEBUG` в env для prod | `app/krl/settings.py` | done |
| TD-2 | В `exercises/__init__.py` в `__all__` указан `ExerciseSchema`, но не импортирован | мелочь | done |
| TD-3 | Свойство `Module.exercise` рекурсивно обращается к себе через `hasattr` | удалён мёртвый property | done |
| TD-4 | Заменить `django-ckeditor` (CKEditor 4 EOL) на `django-ckeditor-5` | низкий приоритет; сейчас `ckeditor.W001`; кастомный plugin `krl_insertbadge`, upload | open |

---

## Как вести

1. Новые идеи — добавлять строкой в таблицы выше с уникальным ID.
2. После реализации — `open` → `done` и ссылка на PR/коммит по желанию.
3. Правила для агентов: `.cursor/rules/`, подробности: `docs/AGENT_KNOWLEDGE.md`.
