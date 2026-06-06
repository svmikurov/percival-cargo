.PHONY: help setup clean format fix lint type-check test test-all ci check prepare-test
.PHONY: run-flask run-flask-debug stop-flask status
.PHONY: docs-build docs-open docs-clean
.PHONY: db-setup db-reset db-shell

# ============================================
# Настройка окружения
# ============================================

setup:
	poetry install

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

# ============================================
# Качество код
# ============================================

format:
	poetry run ruff format

fix:
	poetry run ruff check --fix

lint:
	poetry run ruff check

type-check:
	poetry run mypy .

# ============================================
# Тесты
# ============================================

# Быстрые тесты (без E2E, не требуют сервера)
test:
	poetry run pytest -m 'not e2e'

# Все тесты (требуют запущенный сервер)
test-all:
	poetry run pytest

# Подготовка к тестам (БД + проверки, без запуска сервера)
prepare-test: format fix type-check
	@echo "=== Подготовка базы данных ==="
	sudo -u postgres psql -f setup_db.sql
	@echo "✅ Готово! Теперь:"
	@echo "   1. Запустите сервер: make run-flask"
	@echo "   2. В другом терминале: make test-all"
	@echo "   3. Остановите сервер: make stop-flask"

# ============================================
# CI/CD
# ============================================

# CI проверка (только read-only, без изменений)
ci: lint type-check test

# Полная проверка (с авто-исправлением)
check: format fix type-check test

# ============================================
# База данных
# ============================================

# Создание БД из скрипта
db-setup:
	@echo "Создание базы данных..."
	sudo -u postgres psql -f setup_db.sql
	@echo "✅ База данных готова"

# Полное пересоздание БД (с подтверждением)
db-reset:
	@echo "⚠️  ВНИМАНИЕ! Это удалит ВСЕ данные в базе allocation!"
	@read -p "Вы уверены? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "Пересоздаю базу данных..."; \
		sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'allocation';" 2>/dev/null || true; \
		sudo -u postgres psql -c "DROP DATABASE IF EXISTS allocation;"; \
		sudo -u postgres psql -c "DROP USER IF EXISTS allocation;"; \
		sudo -u postgres psql -f setup_db.sql; \
		echo "✅ База данных пересоздана!"; \
	else \
		echo "Операция отменена"; \
	fi

# Подключение к БД
db-shell:
	sudo -u postgres psql -d allocation

# ============================================
# Flask сервер
# ============================================

# Запуск сервера (обычный режим)
run-flask:
	@echo "Запуск Flask сервера на http://127.0.0.1:5005"
	@echo "Для остановки нажмите Ctrl+C"
	@poetry run flask --app src/percival_cargo/entryponts/flask_app.py run --port 5005

# Запуск с отладкой (auto-reload)
run-flask-debug:
	@echo "Запуск Flask сервера в режиме отладки"
	@poetry run flask --app src/percival_cargo/entryponts/flask_app.py run --port 5005 --debug

# Остановка сервера
stop-flask:
	@echo "Остановка Flask сервера..."
	@pkill -f "flask.*run" 2>/dev/null && echo "✅ Сервер остановлен" || echo "❌ Сервер не запущен"

# Статус сервера
status:
	@if pgrep -f "flask.*run" > /dev/null 2>&1; then \
		echo "✅ Flask сервер ЗАПУЩЕН"; \
		echo "   PID: $$(pgrep -f 'flask.*run')"; \
		echo "   Порт: 5005"; \
		echo "   URL: http://127.0.0.1:5005"; \
	else \
		echo "❌ Flask сервер НЕ ЗАПУЩЕН"; \
	fi

# ============================================
# Документация
# ============================================

docs-build:
	poetry run make -C docs html

docs-open: docs-build
	@xdg-open docs/build/html/index.html 2>/dev/null || \
	 open docs/build/html/index.html 2>/dev/null || \
	 echo "Откройте docs/build/html/index.html в браузере"

docs-clean:
	poetry run make -C docs clean

# ============================================
# Справка
# ============================================

help:
	@echo "=========================================="
	@echo "  Makefile для percival-cargo"
	@echo "=========================================="
	@echo ""
	@echo "📦 Установка и очистка:"
	@echo "  make setup        - Установить зависимости"
	@echo "  make clean        - Удалить кэш-файлы"
	@echo ""
	@echo "🔧 Качество кода:"
	@echo "  make format       - Форматировать код"
	@echo "  make fix          - Исправить ошибки линтера"
	@echo "  make lint         - Проверить код (read-only)"
	@echo "  make type-check   - Проверить типы (mypy)"
	@echo ""
	@echo "🧪 Тесты:"
	@echo "  make test         - Быстрые тесты (без сервера)"
	@echo "  make test-all     - Все тесты (требуют сервер)"
	@echo "  make prepare-test - Подготовить БД + проверки"
	@echo ""
	@echo "🚀 CI и проверки:"
	@echo "  make ci           - CI проверка (read-only)"
	@echo "  make check        - Полная проверка (с исправлениями)"
	@echo ""
	@echo "🐘 База данных:"
	@echo "  make db-setup     - Создать БД из setup_db.sql"
	@echo "  make db-reset     - Пересоздать БД (с подтверждением)"
	@echo "  make db-shell     - Подключиться к БД"
	@echo ""
	@echo "🌐 Flask сервер:"
	@echo "  make run-flask    - Запустить сервер"
	@echo "  make run-flask-debug - Запустить с отладкой"
	@echo "  make stop-flask   - Остановить сервер"
	@echo "  make status       - Статус сервера"
	@echo ""
	@echo "📚 Документация:"
	@echo "  make docs-build   - Собрать документацию"
	@echo "  make docs-open    - Собрать и открыть"
	@echo "  make docs-clean   - Очистить документацию"
	@echo ""
	@echo "📖 Другие команды:"
	@echo "  make help         - Показать эту справку"

# ============================================
# Рекомендации по использованию
# ============================================

# Рекомендуемый workflow для разработки:
#
# 1. Первоначальная настройка:
#    make setup
#    make db-setup
#
# 2. Во время разработки (быстрая проверка):
#    make test          # только быстрые тесты
#    make lint          # проверить стиль кода
#
# 3. Перед коммитом:
#    make check         # полная проверка
#
# 4. Для E2E тестирования:
#    Терминал 1: make run-flask
#    Терминал 2: make test-all
#    Затем: make stop-flask
#
# 5. Если база данных сломалась:
#    make db-reset      # пересоздать БД
#
# 6. CI/CD пайплайн:
#    make ci            # только read-only проверки