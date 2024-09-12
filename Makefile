.PHONY: check
check:
	@echo "🚀 ruff format"
	@-uv run ruff format --check
	@echo "🚀 ruff check"
	@-uv run ruff check

.PHONY: fix
fix:
	@echo "🚀 ruff format"
	@uv run ruff format
	@uv run ruff check --fix

.PHONY: check
typecheck:
	@echo "🚀 mypy"
	@-uv run mypy

.PHONY: test
test:
	@echo "🚀 test"
	@-uv run pytest

.PHONY: encode
encode:
	@echo "🚀 run tests and encode"
	@-uv run pytest -s --skip-mocks encode
