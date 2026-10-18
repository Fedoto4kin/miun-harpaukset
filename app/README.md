## 🚀 **MIUN‑HARPAUKSET — Инструкция деплоя (Prod)**

### 🧩 Структура проекта
- Django backend → контейнер **mhkk_web** (`docker-compose.internal.yml`)
- PostgreSQL → контейнер **mhkk_db**
- Vue frontend → контейнер **mhkk_client** (только для `npm run build`, в runtime не нужен)
- **nginx на хосте** (systemd) → отдаёт SPA из `/var/www/mhkk_client`, проксирует `/api`, `/admin`, `/media`, `/static`

Прод-compose **без** nginx в Docker. Файл `docker-compose-prod.yml` (nginx+certbot в контейнерах) — **legacy**, для текущего прода не использовать.

Compose на сервере всегда с явным файлом:

```bash
docker compose -f docker-compose.internal.yml …
```

Ниже: §1–5 — детали по шагам; §6 — практический деплой изменений кода.

---

## 🗄 1. **Обновление кода**
```bash
cd ~/miun-harpaukset
git pull
```

Если менялись зависимости Python/Node — см. §6 (когда нужен `build` / `npm install`).

---

## 🗃 2. **Пересборка и запуск БД**
Полный сброс (если нужно пересоздать БД) — **осторожно, удаляет данные**:

```bash
docker compose -f docker-compose.internal.yml down -v
docker compose -f docker-compose.internal.yml up -d db
```

Проверка:
```bash
docker compose -f docker-compose.internal.yml logs -f db
```

Ожидаем: `database system is ready to accept connections`.

### 2.1. Миграция PostgreSQL 14 → 16 (одноразово)

Каталог данных `./db` **несовместим** между major-версиями. Нужен dump/restore.
Прод: `docker-compose.internal.yml`, nginx на хосте не трогаем.

```bash
# 1) Бэкап со старого Postgres 14 (пока образ ещё 14, либо временно вернуть image: postgres:14)
docker compose -f docker-compose.internal.yml up -d db
docker compose -f docker-compose.internal.yml exec -T db \
  pg_dump -U "$PG_USER" -d mhkk -Fc -f /tmp/mhkk_pg14.dump
docker compose -f docker-compose.internal.yml cp db:/tmp/mhkk_pg14.dump ./mhkk_pg14.dump

# 2) Остановить стек, убрать старые файлы данных (бэкап каталога на всякий случай)
docker compose -f docker-compose.internal.yml down
sudo mv db "db.pg14.$(date +%Y%m%d)"
mkdir db

# 3) Поднять Postgres 16 (image уже postgres:16 в compose) и восстановить
docker compose -f docker-compose.internal.yml up -d db
# дождаться ready…
docker compose -f docker-compose.internal.yml cp ./mhkk_pg14.dump db:/tmp/mhkk_pg14.dump
docker compose -f docker-compose.internal.yml exec -T db \
  pg_restore -U "$PG_USER" -d mhkk --clean --if-exists /tmp/mhkk_pg14.dump

# 4) Пересобрать/поднять web (Python 3.12 / Django 5.2) и client-сборку
docker compose -f docker-compose.internal.yml build web --no-cache
docker compose -f docker-compose.internal.yml up -d web
docker compose -f docker-compose.internal.yml exec web python manage.py migrate
docker compose -f docker-compose.internal.yml exec web python manage.py collectstatic --noinput
```

Локально (`docker-compose.yml`) — тот же принцип для `./db`.

---

## 🐍 3. **Пересборка и запуск Django**
```bash
docker compose -f docker-compose.internal.yml build web --no-cache
docker compose -f docker-compose.internal.yml up -d web
```

Миграции:
```bash
docker compose -f docker-compose.internal.yml exec web python manage.py migrate
```

Статика Django Admin (если отдаётся через host nginx `/static`):
```bash
docker compose -f docker-compose.internal.yml exec web python manage.py collectstatic --noinput
```

Проверка API:
```bash
curl -I https://karielankieleh.ru/api/
```

---

## 🎨 4. **Сборка фронтенда**
Очистить старый dist (по необходимости):
```bash
rm -rf client/dist
mkdir client/dist
chown krl:krl client/dist
```

Сборка:
```bash
docker compose -f docker-compose.internal.yml run --rm client npm install
docker compose -f docker-compose.internal.yml run --rm client npm run build
```

`npm install` нужен, если менялся `client/package.json` / lockfile; иначе достаточно `npm run build`.

Проверка:
```bash
ls -la client/dist
```

---

## 🌐 5. **Развёртывание фронтенда в nginx (хост)**
Контейнер nginx **не** поднимаем. Копируем билд в каталог, откуда читает systemd-nginx:

```bash
sudo rm -rf /var/www/mhkk_client/*
sudo cp -r client/dist/* /var/www/mhkk_client/
sudo systemctl reload nginx
```

Проверка:
```bash
curl -I https://karielankieleh.ru
```

---

## 🔄 6. **Деплой изменений кода**

### Что выбрать

| Что изменилось | Действия |
|----------------|----------|
| Только Vue (`client/`) | pull → `npm run build` → copy в `/var/www/mhkk_client` → `reload nginx` |
| Django без новых пакетов / без миграций | pull → `up -d web` (том `./app` уже смонтирован; при uWSGI иногда нужен restart) |
| Миграции моделей | pull → `up -d web` → **`migrate`** |
| `requirements.txt` / Dockerfile | pull → **`build web`** → `up -d web` → `migrate` → `collectstatic` |
| `package.json` / lock | pull → **`npm install`** → `npm run build` → copy → reload nginx |
| Типичный релиз (бэк + фронт) | полный цикл ниже или `./upgrade.sh` |

Не делайте `compose down` на проде без нужды — это останавливает БД.  
Не используйте `docker-compose-prod.yml` и не поднимайте nginx из Docker.

### Полный цикл (бэк + фронт)

```bash
cd ~/miun-harpaukset
git pull --ff-only

# Backend
docker compose -f docker-compose.internal.yml build web
docker compose -f docker-compose.internal.yml up -d db web
docker compose -f docker-compose.internal.yml exec -T web python manage.py migrate
docker compose -f docker-compose.internal.yml exec -T web python manage.py collectstatic --noinput

# Frontend → host nginx
docker compose -f docker-compose.internal.yml run --rm client npm install   # если менялись зависимости
docker compose -f docker-compose.internal.yml run --rm client npm run build
sudo rm -rf /var/www/mhkk_client/*
sudo cp -r client/dist/* /var/www/mhkk_client/
sudo systemctl reload nginx
```

Проверки:
```bash
curl -I https://karielankieleh.ru/
curl -I https://karielankieleh.ru/api/
```

### Скрипт `./upgrade.sh`

Тот же полный цикл (internal compose + host nginx). На сервере из корня репо:

```bash
./upgrade.sh                 # бэк + фронт (с npm install)
./upgrade.sh --skip-frontend # только Django (build, migrate, collectstatic)
./upgrade.sh --skip-backend  # только SPA → /var/www/mhkk_client
./upgrade.sh --no-npm-install  # фронт без npm install
```

Репозиторий должен быть чистым (иначе скрипт откажется делать `git pull`).

### Только бэкенд (кратко)

```bash
git pull --ff-only
docker compose -f docker-compose.internal.yml build web   # если менялись зависимости
docker compose -f docker-compose.internal.yml up -d web
docker compose -f docker-compose.internal.yml exec -T web python manage.py migrate
```

### Только фронтенд (кратко)

```bash
git pull --ff-only
docker compose -f docker-compose.internal.yml run --rm client npm run build
sudo rm -rf /var/www/mhkk_client/*
sudo cp -r client/dist/* /var/www/mhkk_client/
sudo systemctl reload nginx
```

---

## 📊 7. **Дамп и загрузка данных**
Создание дампов (на проде — с `docker-compose.internal.yml`):
```bash
docker compose -f docker-compose.internal.yml exec -T web \
  python manage.py dumpdata lessons --indent 4 > app/lessons/fixtures/lessons.json
docker compose -f docker-compose.internal.yml exec -T web \
  python manage.py dumpdata lexicon --indent 4 > app/lexicon/fixtures/lexicon.json
docker compose -f docker-compose.internal.yml exec -T web \
  python manage.py dumpdata grammar --indent 4 > app/grammar/fixtures/grammar.json
```

Загрузка (словарь / грамматика), локально обычно через `docker compose` без `-f`:
```bash
docker compose exec -T web python manage.py loaddata lexicon/fixtures/lexicon.json
docker compose exec -T web python manage.py loaddata grammar/fixtures/grammar.json
```

### Уроки с прода → локально (полный поток, без SSH с локали)

Схема: **прод (dump) → git commit/push → локаль (pull) → `./reload_lessons_fixtures.sh`**.  
Скрипт на локали сам на прод не ходит: нужна уже лежащая фикстура.

**1. Прод — выгрузка** (на сервере, в каталоге проекта):

```bash
cd ~/miun-harpaukset
docker compose -f docker-compose.internal.yml exec -T web \
  python manage.py dumpdata lessons --indent 4 \
  > app/lessons/fixtures/lessons.json
```

**2. Прод — в git:**

```bash
git add app/lessons/fixtures/lessons.json
git commit -m "Update lessons fixtures"
git push
```

**3. Локаль — получение:**

```bash
git pull
```

Файл: `app/lessons/fixtures/lessons.json`.

**4. Локаль — загрузка в БД** (очищает только `lessons`, словарь и grammar не трогает):

```bash
./reload_lessons_fixtures.sh          # спросить → очистить → loaddata
./reload_lessons_fixtures.sh -y       # без подтверждения
./reload_lessons_fixtures.sh --clear-only
```

При загрузке `LessonSpeech.content_type` подгоняется под локальные ContentType.  
Медиа (`media/lessons/*.mp3`) в JSON нет — при необходимости копируйте отдельно.

---

## 🧪 8. **Тесты (backend)**

Локально (dev-compose, контейнер `mhkk_django` / сервис `web`):

```bash
docker compose exec web python manage.py test lexicon.tests lessons.tests --verbosity=2
```

Отдельно:

```bash
# словарь: search_prepare, krl_slugify, word_clean
docker compose exec web python manage.py test lexicon.tests.test_word --verbosity=2

# схемы упражнений + код LessonSpeech (X.Y)
docker compose exec web python manage.py test lessons.tests --verbosity=2

# парсер основ (stem_import)
docker compose exec web python manage.py test lexicon.tests.test_stem_import --verbosity=2
```

На проде тот же `manage.py test`, через `docker compose -f docker-compose.internal.yml exec web …`.

Покрытие сейчас: нормализация `Word`, контракты `ExerciseSchema` (`fill_default` ↔ `validate`), `LessonSpeech.clean`, `stem_import`. Фронтовых тестов пока нет.

---

## 🧹 9. **Очистка системы**
Docker:
```bash
docker system prune -f
docker image prune -a -f
docker builder prune -f
docker container prune -f
docker network prune -f
```

APT:
```bash
sudo apt clean
sudo apt autoclean
sudo apt autoremove --purge
```

Логи:
```bash
sudo journalctl --vacuum-time=7d
```

---