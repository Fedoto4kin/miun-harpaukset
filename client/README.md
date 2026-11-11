# Client (Vue 3 SPA)

## Dev

Из корня репозитория (`docker-compose.yml`):

```bash
docker compose up -d
# Vue dev-server: http://localhost:8080
# API через django: http://localhost:8000  (или через nginx :80)
```

Локальная production-сборка:

```bash
docker compose run --rm client npm run build
# артефакт: client/dist/
```

Без Docker (нужны Node 22+):

```bash
cd client && npm install && npm run serve   # dev
cd client && npm run build                 # dist/
```

## Prod

Сборка и выкладка — на сервере, см. `app/README.md` §6 / `./upgrade.sh`:

1. `docker compose -f docker-compose.internal.yml run --rm client npm run build`
2. Скопировать `client/dist/` → `/var/www/mhkk_client` (host nginx)
3. При отсутствии passwordless `sudo` — копирование через Docker-том (alpine), как в README

## Заметки

- HTTP только через `src/services/*` + `src/axios.js`
- Lookup слова в уроке: `src/components/lessons/WordSelectionLookup.vue` (desktop tip / mobile bottom bar)
- Паттерны: `.cursor/rules/frontend-vue.mdc`
