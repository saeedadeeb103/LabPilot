UV ?= uv
RUN := $(UV) run

.DEFAULT_GOAL := help

.PHONY: help setup format format-check lint typecheck arch test test-unit test-property cov check clean

help: ## List available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

setup: ## Create the virtual environment and install every dependency group
	$(UV) venv --python 3.12
	$(UV) sync --all-groups
	$(RUN) pre-commit install

format: ## Apply formatting and import ordering
	$(RUN) ruff format .
	$(RUN) ruff check --fix .

format-check: ## Verify formatting without writing
	$(RUN) ruff format --check .

lint: ## Run the linter
	$(RUN) ruff check .

typecheck: ## Run strict type checking
	$(RUN) mypy

arch: ## Verify the bounded-context and layering contracts
	$(RUN) lint-imports --config .importlinter

test: ## Run the whole test suite
	$(RUN) pytest

test-unit: ## Run only fast isolated tests
	$(RUN) pytest -m unit

test-property: ## Run only property-based tests
	$(RUN) pytest -m property

cov: ## Run tests with a coverage report
	$(RUN) pytest --cov --cov-report=term-missing

check: format-check lint typecheck arch test ## Run every gate, as CI does

clean: ## Remove build and cache artefacts
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build
	find . -type d -name __pycache__ -not -path './.venv/*' -prune -exec rm -rf {} +
