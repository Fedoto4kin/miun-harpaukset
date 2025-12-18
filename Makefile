.PHONY: format up build shell

format:
	@echo "Formatting code in Docker..."
	docker exec mhkk_django sh -c "python -m isort . && python -m black ."

build:
	@echo "Build project"
	docker compose build

up:
	@echo "Run project"
	docker compose up -d

down:
	@echo "Stop project"
	docker compose down --remove-orphans

shell:
	@echo "Connect to django"
	docker exec -it mhkk_django /bin/bash

# todo: migrations
# todo: shell
# todo: manage.py
# todo: install python packages
# todo: nodejs (client) install dependencies|build for prod
