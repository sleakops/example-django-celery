
TAG="\n\033[0;44m\#\#\# "
END=" \#\#\# \033[0m\n"
SHELL := /bin/bash 

run: ## Run all project
	docker compose up -d

build:
	docker compose build 

reset-db: ## Reset db
	make stop
	-docker container rm django-example-db
	-docker volume rm django-example_db

rebuild-core: ## Rebuild from scratch core project
	-docker image rm -f django-example/core
	-docker container rm django-example-core
	docker compose build core --force-rm 

rebuild-all: ## Rebuild core, db, and console
	make rebuild-core
	make reset-db
	make stop
	make run

recreate: ## Recreate all project
	docker compose up -d --force-recreate

stop: ## Stop all container
	docker compose down

bash: ## Run and attach bash into core container.
	docker compose run --rm --name core-bash core bash

shell: ## Run and attach django shell into core container.
	docker compose run --rm --name core-shell core python manage.py shell

migrate: ## Run and attach django shell into core container.
	docker compose run --rm --name core-shell core python manage.py migrate

makemigrations: ## Run and attach django shell into core container.
	docker compose run --rm --name core-shell core python manage.py makemigrations

createsuperuser: ## Run and attach django createsuperuser into core container.
	docker compose run --rm --name core-createsuperuser core python manage.py createsuperuser

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
