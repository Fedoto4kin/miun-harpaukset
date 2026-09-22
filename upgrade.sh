#!/usr/bin/env bash
# Деплой на прод (актуальная схема).
#
# Compose: docker-compose.internal.yml (web + db + client-для-сборки).
# nginx — на хосте (systemd), статика SPA → /var/www/mhkk_client.
#
# Устарело: docker-compose-prod.yml и сценарий с nginx/certbot в Docker —
# этот скрипт их не использует.
#
# Запуск на сервере из корня репозитория:
#   ./upgrade.sh
#   ./upgrade.sh --skip-frontend
#   ./upgrade.sh --skip-backend
#   ./upgrade.sh --no-npm-install   # только npm run build, без npm install

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

COMPOSE=(docker compose -f docker-compose.internal.yml)
WWW_ROOT="${WWW_ROOT:-/var/www/mhkk_client}"

SKIP_FRONTEND=0
SKIP_BACKEND=0
NPM_INSTALL=1

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \?//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --skip-frontend) SKIP_FRONTEND=1; shift ;;
    --skip-backend) SKIP_BACKEND=1; shift ;;
    --no-npm-install) NPM_INSTALL=0; shift ;;
    *)
      echo "Неизвестный аргумент: $1" >&2
      usage 1
      ;;
  esac
done

if [[ ! -f docker-compose.internal.yml ]]; then
  echo "Нет docker-compose.internal.yml — запускайте из корня репозитория." >&2
  exit 1
fi

echo "=== Проверка git ==="
if ! git diff-index --quiet HEAD --; then
  echo "Репозиторий грязный. Закоммитьте или stash перед деплоем." >&2
  exit 1
fi

echo "=== git pull --ff-only ==="
git pull --ff-only

if [[ "$SKIP_BACKEND" -eq 0 ]]; then
  echo "=== Backend: build + up web ==="
  "${COMPOSE[@]}" build web
  "${COMPOSE[@]}" up -d db web

  echo "=== Backend: migrate ==="
  "${COMPOSE[@]}" exec -T web python manage.py migrate

  echo "=== Backend: collectstatic ==="
  "${COMPOSE[@]}" exec -T web python manage.py collectstatic --noinput
else
  echo "=== Backend пропущен (--skip-backend) ==="
fi

if [[ "$SKIP_FRONTEND" -eq 0 ]]; then
  echo "=== Frontend: сборка ==="
  if [[ "$NPM_INSTALL" -eq 1 ]]; then
    "${COMPOSE[@]}" run --rm client npm install
  fi
  "${COMPOSE[@]}" run --rm client npm run build

  if [[ ! -d client/dist ]] || [[ -z "$(ls -A client/dist 2>/dev/null || true)" ]]; then
    echo "client/dist пуст после сборки — прерывание." >&2
    exit 1
  fi

  echo "=== Frontend: копирование в ${WWW_ROOT} (host nginx) ==="
  sudo mkdir -p "$WWW_ROOT"
  sudo rm -rf "${WWW_ROOT:?}/"*
  sudo cp -r client/dist/* "$WWW_ROOT/"

  echo "=== host nginx: reload ==="
  sudo systemctl reload nginx
else
  echo "=== Frontend пропущен (--skip-frontend) ==="
fi

echo "=== Готово ==="
echo "Проверки:"
echo "  curl -I https://karielankieleh.ru/"
echo "  curl -I https://karielankieleh.ru/api/"
