.PHONY: help \
		venv list outdated tools compile compile/dry sync sync/dry install install-dev dev \
		check fix fmt watch \
		run sh \
		img-dev img-prod img \
		build up up/debug infra infrastructure telemetry \
		down destroy ps start stop restart logs shell psql migrate djshell test

.SILENT: help info venv

.DEFAULT_GOAL := help

ARCH := $(shell uname -m)
PLATFORM :=

PY_VERSION := 3.13
PYENV_PREFIX := $(shell pyenv prefix $(PY_VERSION))
PYENV_PYTHON_BIN := $(PYENV_PREFIX)/bin/python
VENV_DIR := $(CURDIR)/.venv
VENV_PROMPT := online-store
PY := $(VENV_DIR)/bin/python
REPOSITORY := gledi/online-store
CMD := /bin/bash

ifeq ($(ARCH),arm64)
	PLATFORM = --platform linux/amd64
endif

ACTIVATE_INFRASTRUCTURE := $(shell echo $$ACTIVATE_INFRASTRUCTURE_PROFILE)
ACTIVATE_TELEMETRY := $(shell echo $$ACTIVATE_TELEMETRY_PROFILE)

PROFILE_INFRASTRUCTURE :=
PROFILE_TELEMETRY :=

ifeq ($(ACTIVATE_INFRASTRUCTURE),1)
	PROFILE_INFRASTRUCTURE := --profile infrastructure
endif

ifeq ($(ACTIVATE_TELEMETRY),1)
	PROFILE_TELEMETRY := --profile telemetry
endif

PROFILES := --profile app $(PROFILE_INFRASTRUCTURE) $(PROFILE_TELEMETRY)
ALL_PROFILES := --profile app --profile infrastructure --profile telemetry


help:
	echo "Usage: make [target]"
	echo "Targets:"
	echo "  help:                 print this help message"
	echo "  info:                 print environment variables"
	echo "  venv:                 create virtual environment"
	echo "  list:                 list installed packages"
	echo "  outdated:             list outdated packages"
	echo "  tools:                install package & environment management tools"
	echo "  compile:              compile requirements"
	echo "  compile/dry:          dry-run compile requirements"
	echo "  sync:                 sync requirements"
	echo "  sync/dry:             dry-run sync requirements"
	echo "  install:              install package"
	echo "  install-dev:          install package in development mode"
	echo "  dev:                  run all local development tasks"
	echo "  check:                run linter"
	echo "  fix:                  run linter and fix issues"
	echo "  fmt:                  format code"
	echo "  watch:                run linter in watch mode"
	echo "  run:                  run development server"
	echo "  sh:                   run local django shell"
	echo "  img-dev:              build development image"
	echo "  img-prod:             build production image"
	echo "  img:                  build production image"
	echo "  build:                build images"
	echo "  up:                   start all docker compose services for enabled profiles"
	echo "  up/debug:             start docker compose services in debug mode"
	echo "  infra|infrastructure: start infrastructure services"
	echo "  telemetry:            start telemetry services"
	echo "  down:                 stop docker compose services"
	echo "  destroy:              stop docker compose services and remove volumes"
	echo "  ps:                   list docker compose services"
	echo "  start [svc]:          start service (web by default)"
	echo "  stop [svc]:           stop service (web by default)"
	echo "  restart [svc]:        restart service (web by default)"
	echo "  logs [svc]:           show logs for service (web by default)"
	echo "  shell [svc]:          run shell in service (web by default)"
	echo "  psql:                 run psql in db service"
	echo "  migrate:              run migrations"
	echo "  djshell:              run django shell"
	echo "  test:                 run tests"

print-% : ; @echo $* = $($*)

venv:
	if ! [[ -d $(VENV_DIR) ]]; then $(PYENV_PYTHON_BIN) -m venv --prompt=$(VENV_PROMPT) $(VENV_DIR); else echo "$(VENV_DIR) already exists. skipping ..."; fi

list:
	$(PY) -m pip list

outdated:
	$(PY) -m pip list --outdated

tools:
	$(PY) -m pip install --upgrade --upgrade-strategy=eager pip pip-tools

compile:
	$(PY) -m piptools compile --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --all-extras --output-file requirements/dev.txt

compile/dry:
	$(PY) -m piptools compile --dry-run --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --dry-run --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --all-extras --output-file requirements/dev.txt

sync:
	$(PY) -m piptools sync requirements/dev.txt

sync/dry:
	$(PY) -m piptools sync --dry-run requirements/dev.txt

install:
	$(PY) -m pip install --no-deps --use-pep517 .

install-dev:
	$(PY) -m pip install --no-deps --use-pep517 --editable .

dev: tools compile sync install-dev

check:
	$(PY) -m ruff check ./src

fix:
	$(PY) -m ruff check --fix ./src

fmt:
	$(PY) -m ruff format ./src

watch:
	$(PY) -m ruff check --watch ./src

run:
	crosswords runserver

sh:
	crosswords shell_plus

img-dev:
	docker build $(PLATFORM) --tag $(REPOSITORY):dev --target dev .

img img-prod:
	docker build $(PLATFORM) --tag $(REPOSITORY):prod --tag $(REPOSITORY):latest .

build:
	docker compose build --parallel

up:
	docker compose $(PROFILES) up -d

up/debug:
	docker compose $(PROFILES) --file compose.yml --file compose.debug.yml up -d

infra infrastructure:
	docker compose --profile infrastructure up -d

telemetry:
	docker compose --profile telemetry up -d

down:
	docker compose $(ALL_PROFILES) down --remove-orphans --rmi local

destroy:
	docker compose $(ALL_PROFILES) down --remove-orphans --rmi local --volumes

ps:
	docker compose $(ALL_PROFILES) ps --all

start:
	docker compose $(ALL_PROFILES) start $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), web)

stop:
	docker compose $(ALL_PROFILES) stop $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), web)

restart:
	docker compose $(ALL_PROFILES) restart $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), web)

logs:
	docker compose $(ALL_PROFILES) logs -f $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), web)

shell:
	docker compose $(ALL_PROFILES) exec $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), web) $(CMD)

psql:
	docker compose $(ALL_PROFILES) exec db psql -U clues -d crosswords

migrate:
	docker compose $(ALL_PROFILES) exec web crosswords migrate

djshell:
	docker compose $(ALL_PROFILES) exec web python manage.py shell_plus

test:
	docker compose $(ALL_PROFILES) exec web python -m pytest -v .

%:
	@:
