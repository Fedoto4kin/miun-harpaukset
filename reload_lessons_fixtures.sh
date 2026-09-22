#!/usr/bin/env bash
# Очистка локальной БД (только lessons) и загрузка фикстур с прода.
# SSH не нужен: фикстура должна уже лежать локально (git pull / ручное копирование).
#
# Использование:
#   ./reload_lessons_fixtures.sh                 # очистить + загрузить lessons.json
#   ./reload_lessons_fixtures.sh --clear-only    # только очистить
#   ./reload_lessons_fixtures.sh path/to.json    # очистить + загрузить указанный файл
#
# На проде (когда есть доступ к docker на сервере, без SSH с вашей машины —
# например, уже зайдя на хост) дамп:
#   docker compose -f docker-compose.internal.yml exec -T web \
#     python manage.py dumpdata lessons --indent 4 \
#     > app/lessons/fixtures/lessons.json
#
# Затем закоммитить/скачать файл и на локали запустить этот скрипт.
#
# Медиа (mp3) в фикстуре нет — при необходимости скопируйте media/lessons отдельно.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

COMPOSE=(docker compose)
if [[ -f docker-compose.yml ]]; then
  COMPOSE=(docker compose -f docker-compose.yml)
fi

FIXTURE="lessons/fixtures/lessons.json"
CLEAR_ONLY=0
NO_INPUT=0
EXTRA_ARGS=()

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \?//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --clear-only) CLEAR_ONLY=1; shift ;;
    --yes|-y|--no-input) NO_INPUT=1; shift ;;
    -*)
      echo "Неизвестный флаг: $1" >&2
      usage 1
      ;;
    *)
      FIXTURE="$1"
      shift
      ;;
  esac
done

if ! "${COMPOSE[@]}" ps --status running 2>/dev/null | grep -qE 'mhkk_django|[[:space:]]web[[:space:]]'; then
  echo "Контейнер Django не запущен. Поднимите стек: docker compose up -d" >&2
  exit 1
fi

if [[ "$CLEAR_ONLY" -eq 0 ]]; then
  # Путь на хосте для проверки наличия файла
  HOST_FIXTURE="$FIXTURE"
  if [[ "$HOST_FIXTURE" != /* ]]; then
    if [[ -f "app/$HOST_FIXTURE" ]]; then
      HOST_FIXTURE="app/$HOST_FIXTURE"
    elif [[ -f "$HOST_FIXTURE" ]]; then
      :
    else
      echo "Фикстура не найдена: app/$FIXTURE (или $FIXTURE)" >&2
      echo "Сначала положите lessons.json (git pull / копирование с прода)." >&2
      exit 1
    fi
  fi
  echo "Фикстура: $HOST_FIXTURE"
fi

# Подтверждение на хосте: docker exec -T без TTY, django input() не сработает
if [[ "$NO_INPUT" -eq 0 ]]; then
  if [[ "$CLEAR_ONLY" -eq 1 ]]; then
    prompt="Удалить ВСЕ данные lessons из локальной БД? [y/N]: "
  else
    prompt="Очистить lessons и загрузить фикстуру? [y/N]: "
  fi
  read -r -p "$prompt" confirm
  case "$confirm" in
    y|Y|yes|YES) ;;
    *) echo "Отменено."; exit 0 ;;
  esac
fi
EXTRA_ARGS+=(--no-input)

echo "=== Очистка данных lessons ==="
if [[ "$CLEAR_ONLY" -eq 1 ]]; then
  "${COMPOSE[@]}" exec -T web python manage.py clear_lessons "${EXTRA_ARGS[@]}"
  echo "Готово (только очистка)."
  exit 0
fi

# В контейнере cwd=/app, фикстура — lessons/fixtures/...
CONTAINER_FIXTURE="$FIXTURE"
if [[ "$CONTAINER_FIXTURE" == app/* ]]; then
  CONTAINER_FIXTURE="${CONTAINER_FIXTURE#app/}"
fi

echo "=== Очистка + загрузка ==="
"${COMPOSE[@]}" exec -T web \
  python manage.py reload_lessons_fixture "$CONTAINER_FIXTURE" "${EXTRA_ARGS[@]}"

echo "Готово."
