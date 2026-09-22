## 🚀 **MIUN‑HARPAUKSET — Короткая инструкция деплоя (Prod)**

### 🧩 Структура проекта
- Django backend → контейнер **mhkk_web**
- PostgreSQL → контейнер **mhkk_db**
- Vue frontend → контейнер **mhkk_client** (используется только для сборки)
- nginx на хосте → отдаёт `/var/www/mhkk_client`

---

## 🗄 1. **Обновление кода**
```bash
cd ~/miun-harpaukset
git pull
```

Если менялись зависимости — пересобрать контейнеры.

---

## 🗃 2. **Пересборка и запуск БД**
Полный сброс (если нужно пересоздать БД):

```bash
docker compose -f docker-compose.internal.yml down -v
docker compose -f docker-compose.internal.yml up -d db
```

Проверка:
```bash
docker compose -f docker-compose.internal.yml logs -f db
```

Ожидаем: `database system is ready to accept connections`.

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

Проверка API:
```bash
curl -I https://karielankieleh.ru/api/
```

---

## 🎨 4. **Сборка фронтенда**
Очистить старый dist:
```bash
rm -rf client/dist
mkdir client/dist
chown krl:krl client/dist
```

Сборка:
```bash
docker compose -f docker-compose.internal.yml run client npm install
docker compose -f docker-compose.internal.yml run client npm run build
```

Проверка:
```bash
ls -la client/dist
```

---

## 🌐 5. **Развёртывание фронтенда в nginx**
Очистить старый билд:
```bash
sudo rm -rf /var/www/mhkk_client/*
```

Скопировать новый:
```bash
sudo cp -r client/dist/* /var/www/mhkk_client/
```

Перезагрузить nginx:
```bash
sudo systemctl reload nginx
```

Проверка:
```bash
curl -I https://karielankieleh.ru
```

---

## 🔄 6. **Обновление версии (быстрый деплой)**
```bash
cd ~/miun-harpaukset
git pull
docker compose -f docker-compose.internal.yml build web
docker compose -f docker-compose.internal.yml up -d web
docker compose -f docker-compose.internal.yml run client npm run build
sudo rm -rf /var/www/mhkk_client/*
sudo cp -r client/dist/* /var/www/mhkk_client/
sudo systemctl reload nginx
```

---

## 📊 7. **Дамп и загрузка данных**
Создание дампов:
```bash
docker compose exec -it web python manage.py dumpdata lessons --indent 4 > app/lessons/fixtures/lessons.json
docker compose exec -it web python manage.py dumpdata lexicon --indent 4 > app/lexicon/fixtures/lexicon.json
docker compose exec -it web python manage.py dumpdata grammar --indent 4 > app/grammar/fixtures/grammar.json
```

Загрузка (словарь / грамматика):
```bash
docker compose exec -it web python manage.py loaddata lexicon/fixtures/lexicon.json
docker compose exec -it web python manage.py loaddata grammar/fixtures/grammar.json
```

### Уроки с прода → локально (без SSH)

1. На проде снимите дамп `lessons` в `app/lessons/fixtures/lessons.json` (команда выше) и доставьте файл на локаль (git / scp / иное).
2. Локально очистите только `lessons` и загрузите фикстуру:
```bash
./reload_lessons_fixtures.sh          # очистка + loaddata
./reload_lessons_fixtures.sh --clear-only
./reload_lessons_fixtures.sh -y       # без подтверждения
```

Скрипт не ходит на прод по SSH: нужна уже лежащая локально фикстура.  
`LessonSpeech.content_type` при загрузке автоматически подгоняется под локальные ContentType.  
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