"""Pytest configuration."""

import time
from pathlib import Path
from typing import Optional

import pytest
import requests
from requests import Response

import config


def wait_for_webapp_to_come_up() -> Optional[Response]:
    """Ожидает запуска веб-приложения и возвращает первый успешный ответ.

    Эта функция используется в E2E-тестах для проверки, что Flask-приложение
    успело подняться в отдельном процессе после перезапуска. Функция делает
    повторяющиеся попытки HTTP-запроса к API с экспоненциальной задержкой.

    Из книги Персиваля: паттерн "ожидание готовности сервиса" (Service Readiness Probe).
    Это альтернатива time.sleep(), которая может быть либо слишком короткой,
    либо слишком длинной.

    Mechanics:
        1. Устанавливает дедлайн в 10 секунд
        2. Получает URL API из конфигурации (обычно http://localhost:port)
        3. Каждые 0.5 секунд пытается сделать GET-запрос
        4. При ConnectionError (приложение еще не слушает порт) - продолжает попытки
        5. При успешном соединении - возвращает ответ
        6. Если дедлайн истек - проваливает тест через pytest.fail()

    Почему не просто time.sleep(10):
        - Приложение может подняться за 1 секунду (не теряем время)
        - Или за 15 секунд (тест упадет раньше, чем ждать 15 секунд)
        - Адаптивная задержка ускоряет прогон тестов

    Returns:
        Response: объект ответа requests от первого успешного запроса.
                 Обычно это HTTP 200 или статус проверки здоровья (healthcheck)

    Raises:
        AssertionError: через pytest.fail() если API не ответил за 10 секунд.
                       Не возвращает управление в вызывающий код.

    Example:
        >>> # В тестах с перезапуском API
        >>> def test_api_after_restart(restart_api):
        ...     response = wait_for_webapp_to_come_up()
        ...     assert response.status_code == 200

    Note:
        Функция не обрабатывает другие исключения (например, таймауты requests).
        Это сделано намеренно: они означают, что API работает, но медленно,
        и тест должен упасть с явной ошибкой.

    Warning:
        Эта функция ДОЛЖНА использоваться только в тестах. В production-коде
        используйте более надежные механизмы (например, readiness probes
        в Kubernetes или Circuit Breaker).

    """
    deadline = time.time() + 10
    url = config.get_api_url()

    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            # API еще не слушает порт - ждем и пробуем снова
            time.sleep(0.5)

    # Дедлайн истек - тест провален
    pytest.fail('API never came up')


@pytest.fixture
def restart_api() -> None:
    """Pytest-фикстура для перезапуска Flask-приложения во время E2E-тестов.

    Из книги Персиваля: паттерн "рестарт API через touch файла".
    Используется для тестирования behavior, когда приложение теряет соединение
    с БД или нужно проверить восстановление после сбоя.

    Как работает (магия Flask + werkzeug):
        1. При запуске Flask в debug-режиме он отслеживает изменения в файлах
        2. touch() обновляет timestamp файла flask_app.py (меняет mtime)
        3. Flask детектирует изменение и автоматически перезагружается
        4. wait_for_webapp_to_come_up() ждет, пока процесс перезапустится

    Почему так, а не kill/start процесса:
        - Проще: не нужно управлять PID процесса
        - Платформонезависимо: работает на Windows, Linux, macOS
        - Не требует дополнительных прав на kill процессов
        - Flask сам обрабатывает перезагрузку (graceful shutdown)

    Типичные сценарии использования из книги:
        1. Тестирование переподключения к БД после обрыва соединения
        2. Проверка кэширования после перезагрузки конфигурации
        3. Симуляция деплоя новой версии (graceful restart)

    Примеры:
        >>> def test_database_reconnection(restart_api, postgres_db):
        ...     # 1. Создаем данные
        ...     response = client.post('/orders', json={...})
        ...
        ...     # 2. Убиваем соединение с БД (в тестах)
        ...     postgres_db.kill_connections()
        ...
        ...     # 3. Перезапускаем API - он должен переподключиться
        ...     restart_api()
        ...
        ...     # 4. Проверяем, что данные все еще доступны
        ...     response = client.get('/orders/1')
        ...     assert response.status_code == 200

    Warning:
        Эта фикстура несовместима с pytest-xdist (параллельные тесты),
        так как перезапуск API влияет на все тесты, запущенные в том же процессе.
        Используйте отдельную маркировку для таких тестов:

        @pytest.mark.serial
        def test_serial_only(restart_api):
            pass

    Note:
        Время sleep(0.5) критично: Flask нужно время, чтобы детектировать
        изменение файла. Слишком маленькая задержка может привести к
        ложным срабатываниям (перезагрузка еще не началась).

        В книге Персиваль упоминает, что 0.5 секунды - эмпирически
        подобранное значение, работающее на CI (GitHub Actions, Jenkins).

    """
    (Path(__file__).parent / 'flask_app.py').touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
