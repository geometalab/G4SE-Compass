.PHONY: all
all: help

COMPOSE_FILE ?= docker-compose.yml

.PHONY: help
help:
	@echo frequently used:
	@echo "\t"make requirements-upgrade"                           "- upgrade python requirements
	@echo "\t"make build"                                          "- create a new build
#	@echo "\t"make release"                                        "- make a new release
	@echo
	@echo available targets:
	@$(MAKE) --no-print-directory list

.PHONY: list
list:
	@$(MAKE) --no-print-directory _list_targets_on_separate_lines | sed -e 's/^/\t/'

.PHONY: _list_targets_on_separate_lines
_list_targets_on_separate_lines:
# Adopted from http://stackoverflow.com/a/26339924/674064
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	    awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	    sort | \
	    egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: build-frontend
build-frontend:
	docker-compose build frontend && \
	docker-compose run --rm frontend bash -c "npm run build -p && find ./dist -type d -exec chmod 777 {} \; && find ./dist -type f -exec chmod 666 {} \;"

.PHONY: build-backend
build-backend:
	docker-compose build api

.PHONY: build-nginx
build-nginx: build-frontend
	docker-compose build nginx nginx-dev

.PHONY: build
build: build-frontend build-backend build-nginx
	docker-compose build

.PHONY: requirements-upgrade
requirements-upgrade:
	cd compass-api && pip-compile -U dev-requirements.in && pip-compile -U requirements.in

.PHONY: tests
tests: build-backend
	docker-compose run --rm api bash -c "pytest -q --flake8 && pytest"

.PHONY: expectation-tests
expectation-tests:
	docker run --rm --volume=${CURDIR}/expectation_tests:/expectation_tests -it python:3 bash -c "cd /expectation_tests && pip install -r requirements.txt && py.test --host https://search.g4se.hixi.ch"

