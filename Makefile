# Type checking
type-check:
	poetry run mypy .

# Run tests
test:
	poetry run pytest

# Lint code (check only)
lint:
	poetry run ruff check

# Fix lint issues (auto)
fix:
	poetry run ruff check --fix

# Full check (type + lint + test)
check: format fix type-check lint test

# Format code
format:
	poetry run ruff format

# Setup project
setup:
	poetry install

# Clean cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

# Build documentation
docs-build:
	poetry run make -C docs html

# Open documentation with default browser 
docs-open: docs-build
	xdg-open docs/build/html/index.html

# Show all commands
help:
	@echo "Available commands:"
	@echo "  make setup      		- Install dependencies"
	@echo "  make test       		- Run tests"
	@echo "  make lint       		- Check code style"
	@echo "  make fix        		- Auto-fix lint issues"
	@echo "  make type-check 		- Check types (mypy)"
	@echo "  make check      		- Full check with linter format and fix"
	@echo "  make format     		- Format code"
	@echo "  make clean      		- Remove cache files"
	@echo "  make docs-build  		- Remove cache files"
	@echo "  make docs-open			- Build documentation and open via browser"