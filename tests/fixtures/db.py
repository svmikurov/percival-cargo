"""Data base fixtures."""

import time
from typing import Callable, Generator, List, Optional, Tuple

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from percival_cargo import config
from percival_cargo.infrastructure.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db() -> Generator[Engine, None, None]:
    """Create an in-memory SQLite DB engine with all tables created."""
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def session(in_memory_db: Engine) -> Generator[Session, None, None]:
    """Create a new ORM session with mappers configured."""
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


def wait_for_postgres_to_come_up(engine):  # type: ignore
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail('Postgres never came up')


def wait_for_webapp_to_come_up():  # type: ignore
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail('API never came up')


@pytest.fixture(scope='session')
def postgres_db():  # type: ignore
    engine = create_engine(config.get_postgres_url())
    wait_for_postgres_to_come_up(engine)  # type: ignore
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):  # type: ignore
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def add_stock(postgres_session: Session) -> Generator[Callable, None, None]:  # type: ignore
    """Фикстура для добавления тестовых данных (партий товара) в БД с автоматической очисткой.

    Из книги Персиваля: паттерн "тестовый помощник с обратным действием" (test helper with teardown).

    Зачем это нужно:
        - Интеграционные тесты требуют реальной БД для проверки SQL-запросов
        - Но после каждого теста нужно очищать данные, чтобы тесты не влияли друг на друга
        - Вместо ручного удаления в каждом тесте, фикстура запоминает, что добавила, и удаляет

    Как работает:
        1. Setup (до yield): создает внутренние множества для отслеживания ID
        2. Определяет внутреннюю функцию _add_stock для добавления данных
        3. Yield возвращает эту функцию тесту
        4. Teardown (после yield): удаляет все добавленные данные в правильном порядке

    Почему такое сложное удаление (batches → allocations → order_lines):
        - Таблицы связаны внешними ключами
        - Сначала нужно удалить allocations (дочерние записи)
        - Потом batches (родительские записи)
        - И только потом order_lines (могут быть независимыми)
        - Нельзя просто TRUNCATE, т.к. тесты могут запускаться параллельно

    Args:
        postgres_session: Фикстура с реальной сессией PostgreSQL

    Yields:
        Callable: Функция _add_stock(lines), где lines - список кортежей
                 (ref, sku, qty, eta)

    Example:
        >>> def test_allocate_from_batch(add_stock, postgres_session):
        ...     # Добавляем тестовые данные
        ...     add_stock([
        ...         ('BATCH-001', 'RED-CHAIR', 10, datetime(2024, 1, 1)),
        ...         ('BATCH-002', 'BLUE-TABLE', 5, None),  # None = без даты
        ...     ])
        ...
        ...     # Тестируем аллокацию
        ...     allocate('order-1', 'RED-CHAIR', 3, postgres_session)
        ...
        ...     # Проверяем результат
        ...     result = postgres_session.execute(
        ...         "SELECT sku, quantity FROM allocations JOIN ..."
        ...     ).fetchone()
        ...     assert result.quantity == 3
        ...
        ...     # Данные автоматически удалятся после теста

    Note:
        Фикстура использует postgres_session.commit() после вставки,
        потому что реальная БД требует коммита для видимости данных в других запросах.

        В отличие от unit-тестов с фейковым репозиторием, здесь НЕЛЬЗЯ
        использовать rollback, потому что тест может делать несколько коммитов.

    Warning:
        Фикстура НЕ потокобезопасна! Если тесты запускаются параллельно
        (pytest-xdist), то разные тесты могут добавлять одинаковые reference.
        Решение: использовать уникальные суффиксы (test_UUID) или транзакционные
        тесты (очистка через SAVEPOINT).

    """
    batches_added = set()  # Храним ID добавленных партий
    skus_added = set()  # Храним SKU для очистки order_lines

    def _add_stock(lines: List[Tuple[str, str, int, Optional[str]]]) -> None:
        """Вспомогательная функция для добавления stock в БД.

        Args:
            lines: Список кортежей (reference, sku, quantity, eta)
                  eta может быть строкой даты ISO или None

        """
        for ref, sku, qty, eta in lines:
            # 1. Вставляем партию (batch)
            postgres_session.execute(
                text(
                    'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
                    ' VALUES (:ref, :sku, :qty, :eta)'
                ),
                dict(
                    ref=ref,
                    sku=sku,
                    qty=qty,
                    eta=eta,
                ),
            )

            # 2. Получаем автоматически сгенерированный ID
            [[batch_id]] = postgres_session.execute(
                text(
                    'SELECT id FROM batches WHERE reference=:ref AND sku=:sku'
                ),
                dict(ref=ref, sku=sku),
            )

            # 3. Запоминаем ID для последующей очистки
            batches_added.add(batch_id)
            skus_added.add(sku)

        # 4. Фиксируем изменения в БД
        postgres_session.commit()

    # Возвращаем функцию тесту
    yield _add_stock

    # --- TEARDOWN (очистка после теста) ---

    # Удаляем allocations (дочерние записи, ссылающиеся на batches)
    for batch_id in batches_added:
        postgres_session.execute(
            text('DELETE FROM allocations WHERE batch_id=:batch_id'),
            dict(batch_id=batch_id),
        )
        # Удаляем сами batches
        postgres_session.execute(
            text('DELETE FROM batches WHERE id=:batch_id'),
            dict(batch_id=batch_id),
        )

    # Удаляем order_lines (могут быть независимы от batches)
    for sku in skus_added:
        postgres_session.execute(
            text('DELETE FROM order_lines WHERE sku=:sku'),
            dict(sku=sku),
        )

    # Фиксируем очистку
    postgres_session.commit()
