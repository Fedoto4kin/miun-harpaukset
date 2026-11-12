# Слитные сложения (lookup fallback)

**Статус:** v1 закрыта (2026-11). Runtime-only: фикстуры / generate не трогаем.

Граница в орфографии **не** размечена (нет дефиса и `|` в запросе). Режем по словарю: позиция, где **обе** части — известные `form_clean` / `word_clean`.

## Поток

1. `SearchViewList` — `search_prepare` → exact лемма/форма.
2. Exact hits → как раньше, разрез **не** вызывается (`pitkäkieli`, `šyöndäpaikka`).
3. Пусто → `find_best_compound_split(prepared)`.
4. Лучший разрез → два (или больше) exact-хита по частям + meta:
   - `compound_parts: ["muamon", "kieli"]`
   - `compound_of: "muamonkieli"`
5. UI: баннер `A + B` в `LexiconComponent` и `WordSearchPopupComponent`.

Не участвует: `?letter=`, prefix-suggestions, парадигма, generate/фикстуры.

## Код

| Файл | Роль |
|------|------|
| `lexicon/compound_split.py` | кандидаты, batch lookup, скоринг |
| `api_v0/lexiconViews/SearchViewList.py` | hook после 0 exact |
| `api_v0/serializers/lexicon_serializers.py` | `compound_parts` / `compound_of` |
| `lexicon/tests/test_compound_split.py` | unit + API |
| client: `LexiconComponent.vue`, `WordSearchPopupComponent.vue` | баннер `A + B` |

## Тюнинг при ложных разрезах

| Рычаг | Где | Сейчас | Когда крутить |
|-------|-----|--------|----------------|
| `MIN_PART_LEN` | `compound_split.py` | `3` | слишком короткие мусорные части |
| бонус головы `nom_sg` / лемма | `score_split` (+100) | правый = голова | голова не выбирается |
| бонус левого `-n` | `score_split` (+40) | gen-связка | gen проигрывает без `-n` типу |
| tie-break | sort: длиннее right, затем left | разрез правее | ничья не в пользу головы |
| known surfaces | `form_clean` **и** `word_clean` | обе части обязаны быть в словаре | одна часть «есть», другой нет → пусто |

Эталоны учебника: `muamonkieli` → `muamon|kieli`; `eländäpaikka` → `eländä|paikka`.

## Тесты

```bash
docker compose exec -T web python manage.py test lexicon.tests.test_compound_split -v2
```

Кейсы: `muamonkieli`, `eländäpaikka`, exact `pitkäkieli` без разреза, короткий/unknown → пусто.

Прод-smoke: `GET /api/v0/lexicon/search/?query=muamonkieli` → `compound_parts`.

## Вне v1 / известные края

- 3+ члена (`a+b+c`) — не режем рекурсивно.
- Дефисные написания — не нормализуем отдельно.
- Несколько `Word` на одну поверхность части → несколько карточек (напр. дубли `paikka`); дедуп только по `word.id`.
- RAM-кэш всего множества форм — не нужен, пока batch `__in` не замерзнет.
- Suggestions не делают compound-fallback (только exact search / lesson lookup через search).

При баге: сначала добавить кейс в `test_compound_split.py`, потом крутить скоринг/`MIN_PART_LEN`, не размазывать логику по UI.
