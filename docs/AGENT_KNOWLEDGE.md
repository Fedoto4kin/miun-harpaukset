# База знаний для агентов — Miun harpaukšet karielan kieleh

Краткий справочник по проекту. Правила Cursor в `.cursor/rules/` подхватывают сжатые версии автоматически.

## 1. Назначение

Цифровая версия учебника тверского карельского (угрожаемый язык). Функции:

- словарь (прямой / обратный поиск, карточки, словоформы/парадигма, озвучка);
- уроки с модулями (HTML + аудио + упражнения + грамматический комментарий);
- грамматические таблицы.

## 2. Карта каталогов

```
miun-harpaukset/
├── app/                      # Django
│   ├── krl/                  # settings, urls, wsgi
│   ├── lexicon/              # модели словаря
│   ├── lessons/              # уроки, модули, упражнения, admin
│   │   ├── exercises/        # JSON Schema контракты типов
│   │   ├── models/
│   │   ├── admin/
│   │   └── fixtures/
│   ├── grammar/              # GrammarTable
│   ├── api_v0/               # REST API
│   └── requirements.txt
├── client/                   # Vue 3 SPA
│   └── src/
│       ├── components/
│       ├── services/
│       ├── router/
│       └── mixins/
├── services/                 # Docker + nginx
├── docker-compose.yml        # local dev
├── docker-compose.internal.yml  # prod-like
├── backlog.md
└── .cursor/rules/            # правила агентов
```

## 3. Модели предметной области

### Lessons

```
Lesson (number, title, slogan, description, is_enabled)
  └── Module (number, html_content, tags)
        ├── Exercise[] (exercise_type, data JSON, has_answers_check)
        ├── GrammarComment? (OneToOne, html_content, lang, summary)
        └── LessonSpeech? (GenericFK: Lesson | Module)
```

`Module.html_content` может содержать плейсхолдер `[[widget:lesson_cover]]`.

### Lexicon

```
Word (word, word_clean, variant, additional, pos, speech, alias M2M)
  ├── Definition[] (lang: ru|fi, definition)
  ├── Stem[]          # основы из <code> в orig (+ pronouns)
  └── WordForm[]      # сгенерированные формы; alt_spellings — только поиск
GrammarForm           # слоты парадигмы (code, name_krl/ru, category)
Pos, Speech (медиа)
```

Алфавит: `ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ`. Нормализация: lower, `ü`→`y`, мягкий знак → снятие (`lexicon.ortho`, канон U+02BC).

Поиск: `?query=` — exact лемма/форма/альт; `?letter=` — алфавитная лента по лемме.  
Подсказки: префикс + чипы по веткам; уникальная точная форма → цепочка form→лемма.  
Оффлайн fill: `import_stems` / `import_pronouns` / `generate_wordforms` / `generate_diminutives`; парадигма на прод — `loaddata` фикстуры (`dim_*` в фикстуре — `MORPH-10`).  
`GrammarForm.category=diminutive` — только поиск/цепочки, не таблица парадигмы. Ярлыки глаголов — TERMINAT/учебник. Детали: `.cursor/rules/lexicon-morphology.mdc`, `backlog.md` → MORPH-*.

### Grammar

`GrammarTable(title, html_content, order, is_published)` — отдельно от комментариев в модулях.

## 4. REST API (`/api/v0/`)

| Метод | Путь | Назначение |
|-------|------|------------|
| GET | `/lessons/` | список уроков |
| GET | `/modules/` | модули |
| GET | `/modules/by-lesson/{id}/` | модули урока |
| GET | `/modules/{id}/content/` | полный контент модуля |
| GET | `/lexicon/search/` | поиск (`query` exact / `letter` browse) |
| GET | `/lexicon/reverse/` | обратный поиск |
| GET | `/lexicon/search-suggestions/` | подсказки |
| GET | `/lexicon/grouped-search-suggestions/` | подсказки + чипы форм |
| GET | `/lexicon/reverse-search-suggestions/` | подсказки reverse |
| GET | `/lexicon/word-card/{id}/` | карточка слова |
| GET | `/lexicon/word-card/{id}/paradigm/` | парадигма словоформ |
| GET | `/lexicon/pos/` | части речи |
| GET | `/grammar/`, `/grammar/{id}/` | таблицы |

API в основном **read-only**. Запись — через Django Admin.

## 5. Типы упражнений

| `exercise_type` | Backend schema | Vue component |
|-----------------|----------------|---------------|
| InteractiveHint | InteractiveHintExercise | InteractiveHintExerciseComponent |
| FillBlank | FillBlankExercise | FillBlankExerciseComponent |
| SyllableAssembly | SyllableAssemblyExercise | SyllableAssemblyExerciseComponent |
| FillBlankText | FillBlankTextExercise | FillBlankTextExerciseComponent |
| SentenceAssembly | SentenceAssemblySimpleExercise | SentenceAssemblyExerciseComponent |
| SentenceAssemblyPrefilled | SentenceAssemblyPrefilledExercise | SentenceAssemblyPrefilledComponent |
| MatchPair | MatchPairExercise | MatchPairExerciseComponent |
| MatchPairMultiple | MatchPairMultipleExercise | MatchPairMultiplyExerciseComponent |
| FillBlankTable | FillBlankTableExercise | FillBlankTableExerciseComponent |
| MatchPairSentenceSlot | MatchPairSlotsExercise | MatchPairSentenceSlotExerciseComponent |
| FillGapWithChoice | FillGapWithChoiceExercise | FillGapWithChoiceExerciseComponent |
| FillWord | FillWordExercise | FillWordExerciseComponent |

Чеклист нового типа — в `.cursor/rules/exercises.mdc`.

## 6. Frontend-маршруты

| Path | Компонент |
|------|-----------|
| `/` | HomeComponent |
| `/lexicon`, `/lexicon/:letter`, `/lexicon/search/:query`, `/lexicon/translate/:query` | LexiconComponent |
| `/lessons/:id?/:moduleId?` | LessonsComponent |
| `/grammar/:id` | GrammarTableDetail |
| `/authors`, `/books` | Authors / Books |
| `*` | NotFound |

## 7. Dev / Prod

**Стек:** Python 3.12, Django 5.2 LTS, PostgreSQL 16, Node 22, Vue 3.

**Local (`docker-compose.yml`):** nginx:80, django:8000, vue serve:8080, postgres, pgadmin:5050.

**Prod (`docker-compose.internal.yml` + host nginx):** контейнеры `mhkk_web`, `mhkk_db`, build-only `mhkk_client`; статика копируется в `/var/www/mhkk_client`. Инструкции — `app/README.md`. Апгрейд PG major — dump/restore (§2.1 в README).

## 8. Админка

- Nested admin для Lesson → Module → Exercise / Speech / GrammarComment
- Exercise.data — JSONEditorWidget
- Module.html_content — CKEditor (+ кастомный plugin `krl_insertbadge`)
- Кнопки «+ Pagina» для привязки аудио

## 9. Соглашения при разработке

1. Сохранять существующие имена `exercise_type` и форму JSON.
2. HTTP-логику клиента держать в `services/`.
3. Карельский UI-текст и verbose_name не «русифицировать» без запроса.
4. Не коммитить секреты. `DEBUG` / `DJANGO_SECRET_KEY` — из env (compose); insecure fallback только при `DEBUG=True`.
5. Документация деплоя — на русском в `app/README.md`.
