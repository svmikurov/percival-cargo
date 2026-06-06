"""Configuration."""

import os


def get_postgres_uri() -> str:
    """Возвращает URI подключения к PostgreSQL с учетом окружения (local vs production).

    Из книги Персиваля: паттерн "конфигурация через переменные окружения с умолчаниями".
    Это позволяет запускать код без настройки (локально) и в production без изменений.

    Особенности из книги:
        - Локально: PostgreSQL на порту 54321 (чтобы не конфликтовать с системным)
        - В CI/production: стандартный порт 5432
        - Пароль по умолчанию 'abc123' - специально небезопасный, чтобы заметить,
          если забыли переопределить через DB_PASSWORD в production

    Returns:
        str: Строка подключения в формате:
             postgresql://user:password@host:port/database

    Example:
        >>> # Локальный запуск (без переменных окружения)
        >>> os.environ.pop('DB_HOST', None)  # удаляем, если есть
        >>> get_postgres_uri()
        'postgresql://allocation:abc123@localhost:54321/allocation'

        >>> # Production с переменными
        >>> os.environ['DB_HOST'] = 'prod-db.example.com'
        >>> os.environ['DB_PASSWORD'] = 'secure_password_123'
        >>> get_postgres_uri()
        'postgresql://allocation:secure_password_123@prod-db.example.com:5432/allocation'

    Warning:
        Никогда не используйте значения по умолчанию в production!
        Всегда переопределяйте DB_PASSWORD и DB_HOST через переменные окружения.

    Note:
        Нестандартный порт 54321 для localhost выбран, чтобы:
        1. Не требовать прав root (стандартный порт 5432 может быть занят)
        2. Избежать конфликта с системным PostgreSQL, если он установлен
        3. Сделать явным, что это тестовый экземпляр

    """
    host = os.environ.get('DB_HOST', 'localhost')
    # Магия: если хост localhost -> порт 54321, иначе production порт 5432
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'allocation', 'allocation'
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


def get_api_url() -> str:
    """Формирует URL для доступа к API с учетом окружения (local vs production).

    Из книги Персиваля: единый способ получения URL API во всех тестах и клиентах.

    Логика портов из книги:
        - Локально (localhost): порт 5005 (стандартный порт Flask для разработки)
        - В production: порт 80 (HTTP) или 443 (HTTPS - нужно настраивать отдельно)

    Почему разные порты для local/production:
        1. Локально: 5005 не требует sudo и не конфликтует с другими сервисами
        2. В production: порт 80 - стандартный для веб-серверов
        3. Тесты используют localhost:5005, CI использует API_HOST через переменную

    Returns:
        str: URL в формате http://host:port

    Example:
        >>> # Локальная разработка
        >>> get_api_url()
        'http://localhost:5005'

        >>> # Деплой на сервер
        >>> os.environ['API_HOST'] = 'api.mycompany.com'
        >>> get_api_url()
        'http://api.mycompany.com:80'

        >>> # Kubernetes с сервисом на порту 80
        >>> os.environ['API_HOST'] = 'allocation-service.default.svc.cluster.local'
        >>> get_api_url()
        'http://allocation-service.default.svc.cluster.local:80'

    Warning:
        Эта функция возвращает HTTP, а не HTTPS!
        В реальном production нужно:
        1. Либо использовать HTTPS через обратный прокси (nginx/traefik)
        2. Либо явно задавать протокол через переменную API_PROTOCOL

        Пример расширения:
            protocol = os.environ.get('API_PROTOCOL', 'http')
            return f'{protocol}://{host}:{port}'

    Note:
        Порты фиксированные, в отличие от БД:
        - API порт 80 стандартный, его редко меняют
        - БД порт может быть разным (распространенная практика в облаках)

    """
    host = os.environ.get('API_HOST', 'localhost')
    port = 5005 if host == 'localhost' else 80
    return f'http://{host}:{port}'
