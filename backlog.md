# Бэклог — Miun harpaukšet

Собрано из `backlog.md`, TODO в коде и незакрытых заметок в README. Статусы: `open` | `done`.

---

## UX / продукт

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| UX-1 | При скролле страницы урока держать аудиоплеер видимым (sticky/fixed) | `LessonHeaderComponent.vue` | done |
| UX-2 | Выставлять `document.title` с номером модуля при навигации по урокам | `LessonsComponent.vue` | done |
| UX-3 | Lookup слова из текста урока на touch: тап → нижняя панель (не selection-tip под системным меню) | `WordSelectionLookup.vue` | done |

## Контент / упражнения

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| EX-1 | Добавить `title` в схему FillBlankText | `fill_blank_text_exercise.py` | done |

## Лексикон / backend

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| LX-1 | Вынести `Word.search_prepare` в сервисный слой | `lexicon/search.py` | done |
| LX-2 | Фильтровать ввод поиска по `KRL_ABC` | `lexicon/search.py` | done |

## Морфология словаря

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| MORPH-CORE | Stem/WordForm для `s.`/`a.`/`pron.`/`v.`, поиск по формам, попап парадигмы, подсказки с чипами, `alt_spellings`, selection в уроках, фикстура на прод | `lexicon/*`, `api_v0`, client | done |
| MORPH-DIM | Продуктивные уменьшительные `s.` на `-ne` (поиск-цепочка; не в таблице парадигмы); skip при sibling `*ne` | `wordform_gen/diminutives`, `generate_diminutives` | done |
| MORPH-LABELS | Ярлыки глаголов `name_krl` по TERMINAT/учебнику (`prezensa`, `kondicionala`, `pričastija`/`aktiva`/`passiva`); фин. `myönteinen`/`kieltävä`, `1.yks.`/`1.mon.` оставлены | `rules_verbs*`, fixtures, `ParadigmPopup` | done |
| MORPH-POSS | Притяжательные `-ni`/`-š` (+ `-zeni`/`-zeš`) для поиска; не в таблице парадигмы; ярлыки `omistuš` / `pieniskö` | `wordform_gen/possessives`, `generate_possessives`; прод ~5.5k | done |

Закрыто (2026-11): импорт основ + генерация словоформ; exact search + `?letter=`; grouped suggestions (префикс → чипы, уникальная форма → цепочка); парадигма на карточке; lesson popup (desktop selection / mobile tap+bar); notranslate; базовая парадигма через `lexicon.json` `loaddata`. Ручные альты: `käyvä` `kävin`/`kävit`. Уменьшительные (~36k) и притяжательные (~5.5k) — в фикстуре и на проде (`MORPH-DIM` / `MORPH-POSS` / `MORPH-10`).

### Остаточные расхождения (не блокеры)

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
| MORPH-10 | Dims + possessives в фикстуре | `lexicon.json` включает `dim_*` (~36k) и `poss_*` (~5.5k); прод — `loaddata` (без generate на сервере) | done |
| MORPH-STEM-AUDIT | Аудит основ s.: структура + Dictorpus d47 + книга; точечный `regen_lemma` | `lexicon/stem_audit`, `audit_stems`, `regen_lemma` | done |

## Документация / DX

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| DX-1 | Описать setup client (dev и prod) в `client/README.md` | `client/README.md` | done |
| DX-2 | Указать лицензию в корневом README | `README.md` | open |
| DX-3 | Удалить legacy: `fixutres.sh`, `letencrypypt.sh`, `docker-compose-prod.yml` | ревизия 2026-11 | done |
| DX-4 | Миграция на `GrammarForm.Category.DIMINUTIVE` (choices; схемы нет, Django ругается при migrate) | `grammar_form.py`, `0031_grammarform_category_choices` | done |
| DX-5 | WIP ASR в `.gitignore`: `asr_bench/`, `export_asr_gold`/`run_asr_bench`, `requirements-asr-bench.txt`, `voice-input-project.md` — локально сохраняем до решения по голосовому вводу | voice input | open |

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
