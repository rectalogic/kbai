.PHONY: check
check:
	@echo "🚀 ruff format"
	@uv run ruff format --check
	@echo "🚀 ruff check"
	@uv run ruff check

.PHONY: fix
fix:
	@echo "🚀 ruff format"
	@uv run ruff format
	@uv run ruff check --fix
