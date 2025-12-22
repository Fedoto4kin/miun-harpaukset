.PHONY: code-format up build shell django-manage

code-format:
	@echo "Formatting code in Docker..."
	docker exec mhkk_django sh -c "python -m isort . && python -m black ."

build:
	@echo "Build project"
	docker compose build

up:
	@echo "Run project"
	docker compose up -d --remove-orphans

down:
	@echo "Stop project"
	docker compose down --remove-orphans

shell:
	@echo "Connect to django service"
	docker exec -it mhkk_django /bin/bash

# docker exec -it mhkk_django python manage.py $(ARGS)

# todo: migrations
# todo: manage.py
# todo: install python packages
# todo: nodejs (client) install dependencies|build for prod
