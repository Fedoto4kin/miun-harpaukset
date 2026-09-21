# Бэклог — Miun harpaukšet

Собрано из `backlog.md`, TODO в коде и незакрытых заметок в README. Статусы: `open` | `done`.

---

## UX / продукт

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| UX-1 | При скролле страницы урока держать аудиоплеер видимым (sticky/fixed) | `backlog.md` | open |
| UX-2 | Выставлять `document.title` с номером модуля при навигации по урокам | `LessonsComponent.vue` | open |

## Контент / упражнения

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| EX-1 | Добавить `title` в схему FillBlankText | `fill_blank_text_exercise.py` | open |

## Лексикон / backend

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| LX-1 | Вынести `Word.search_prepare` в сервисный слой | `lexicon/models/word.py` | open |
| LX-2 | Фильтровать ввод поиска по `KRL_ABC` | `lexicon/models/word.py` | open |

## Документация / DX

| ID | Задача | Источник | Статус |
|----|--------|----------|--------|
| DX-1 | Описать setup client (dev и prod) в `client/README.md` | `client/README.md` `@todo` | open |
| DX-2 | Указать лицензию в корневом README | `README.md` | open |

## Техдолг (зафиксировано при обзоре, не из TODO)

| ID | Задача | Примечание | Статус |
|----|--------|------------|--------|
| TD-1 | Вынести `SECRET_KEY` / `DEBUG` в env для prod | `app/krl/settings.py` | open |
| TD-2 | В `exercises/__init__.py` в `__all__` указан `ExerciseSchema`, но не импортирован | мелочь | open |
| TD-3 | Свойство `Module.exercise` рекурсивно обращается к себе через `hasattr` | вероятно баг/мертвый код | open |

---

## Как вести

1. Новые идеи — добавлять строкой в таблицы выше с уникальным ID.
2. После реализации — `open` → `done` и ссылка на PR/коммит по желанию.
3. Правила для агентов: `.cursor/rules/`, подробности: `docs/AGENT_KNOWLEDGE.md`.
