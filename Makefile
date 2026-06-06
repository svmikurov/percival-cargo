# Check types (mypy)
type-check:
	poetry run mypy .

# Run tests
test:
	poetry run pytest

# Lint code (read-only, no fixes)
lint:
	poetry run ruff check

# Auto-fix lint issues
fix:
	poetry run ruff check --fix

# CI pipeline (read-only checks, no changes)
ci: lint type-check test

# Full pre-commit check (format + fix + type-check + test)
check: format fix type-check test

# Format code
format:
	poetry run ruff format

# Install dependencies
setup:
	poetry install

# Remove cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

# Build documentation (HTML)
docs-build:
	poetry run make -C docs html

# Build docs and open in default browser
docs-open: docs-build
	xdg-open docs/build/html/index.html

# Run flask server
run-flask:
	@poetry run flask --app src/percival_cargo/entryponts/flask_app/app.py run --port 5005

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make setup        - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Check code style (read-only)"
	@echo "  make fix          - Auto-fix lint issues"
	@echo "  make type-check   - Check types with mypy"
	@echo "  make format       - Format code with ruff"
	@echo "  make check        - Full check (format + fix + type-check + test)"
	@echo "  make ci           - CI check (read-only: lint + type-check + test)"
	@echo "  make clean        - Remove cache files"
	@echo "  make docs-build   - Build HTML documentation"
	@echo "  make docs-open    - Build docs and open in browser"
	@echo "  ----- Flask -----"
	@echo "  make run-flask    - ..."
