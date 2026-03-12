.PHONY: check-lint test setupt setup lint install clean

setup_file_path := $(PWD)/setup.sh

setupt:
	@if ! [ -x "$(setup_file_path)" ]; then \
		chmod +x ./setup.sh; \
	fi
	@./setup.sh

install:
	uv sync
	uv run python -m ipykernel install --user --name=ad-kernel

setup: install

check-lint:
	uv run black --check .
	uv run ruff check .

lint:
	uv run black .
	uv run ruff check --fix .

test:
	uv run coverage run --branch --source=./openad -m pytest --durations=10 --color=yes tests/
	uv run coverage report

test-unit:
	uv run pytest tests/unit/ -v

test-imports:
	uv run pytest tests/unit/test_imports.py -v

test-helpers:
	uv run pytest tests/unit/test_helpers.py -v

test-api:
	uv run pytest tests/unit/test_api.py -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build

type-check:
	uv run mypy openad/ --ignore-missing-imports

pre-commit:
	uv run pre-commit run --all-files
