.PHONY: check list outdated tools compile sync build install install-dev dev build prerun run cleanup img img-dev up down destroy ps top start stop logs shell djshell test

.SILENT: check venv compile

PY_VERSION = 3.13
PYENV_PREFIX = $(shell pyenv prefix $(PY_VERSION))
PYENV_PYTHON_BIN = $(PYENV_PREFIX)/bin/python
VENV_DIR = .venv
PYTHON = ./$(VENV_DIR)/bin/python
REPOSITORY = gledi/store
TAG = develop
SVC = web
REQUIREMENTS = dev
CMD = bash

check:
	echo "PY_VERSION =" $(PY_VERSION)
	echo "PYENV_PREFIX =" $(PYENV_PREFIX)
	echo "PYENV_PYTHON_BIN =" $(PYENV_PYTHON_BIN)
	echo "REPOSITORY =" $(REPOSITORY)
	echo "TAG =" $(TAG)
	echo "SVC =" $(SVC)
	echo "CMD =" $(CMD)
	echo "REQUIREMENTS =" $(REQUIREMENTS)

venv:
	if ! [[ -d $(VENV_DIR) ]]; then $(PYENV_PYTHON_BIN) -m venv --prompt=online-store $(VENV_DIR); else echo "$(VENV_DIR) already exists. skipping virtualenv creation ..."; fi

list:
	$(PYTHON) -m pip list

outdated:
	$(PYTHON) -m pip list --outdated

tools:
	$(PYTHON) -m pip install --upgrade --upgrade-strategy=eager pip pip-tools

compile:
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --extra=prod --output-file requirements/prod.txt
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --all-extras --output-file requirements/dev.txt

sync:
	$(PYTHON) -m piptools sync requirements/$(REQUIREMENTS).txt

install:
	$(PYTHON) -m pip install --no-deps .

install-dev:
	$(PYTHON) -m pip install --no-deps --editable .

dev: tools compile sync install-dev

build:
	$(PYTHON) --version

prerun:
	if [[ "$(shell docker ps -aq --filter name=store-cache)" != "" ]]; then docker rm -f store-cache; fi
	if [[ "$(shell docker ps -aq --filter name=store-db)" != "" ]]; then docker rm -f store-db; fi
	if [[ "$(shell docker volume ls --filter name=store_local_dbdata)" == "" ]]; then docker volume create store_local_dbdata; fi
	docker run --rm --name=store-cache -p 26379:6379 -d redis:7.2-alpine
	docker run --rm --name=store-db -p 25432:5432 -v store_local_dbdata:/var/lib/postgresql/data -e PGTZ=UTC -e POSTGRES_DB=storedb -e POSTGRES_USER=sell -e POSTGRES_PASSWORD=stuff -d postgres:16-alpine

run:
	$(PYTHON) store/manage.py runserver

cleanup:
	docker stop store-cache store-db

img:
	docker build --tag $(REPOSITORY):prod --tag $(REPOSITORY):latest --force-rm $(USE_CACHE) .

img-dev:
	docker build --tag $(REPOSITORY):develop --force-rm $(USE_CACHE) .

up:
	docker compose up --build -d

down:
	docker compose down --remove-orphans --rmi local

destroy:
	docker compose down --remove-orphans --rmi local --volumes

ps:
	docker compose ps

top:
	docker compose top $(SVC)

start:
	docker compose start $(SVC)

stop:
	docker compose stop $(SVC)

logs:
	docker compose logs -f $(SVC)

shell:
	docker compose exec $(SVC) $(CMD)

djshell:
	docker compose exec web python manage.py shell_plus

test:
	docker compose run --rm web python -m pytest -v
