"""Pytest configuration."""

from collections.abc import Generator
from datetime import date, timedelta

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from percival_cargo.infrastructure.orm import metadata, start_mappers

###################################################
# Dates
###################################################


@pytest.fixture
def today() -> date:
    """Provide the today date."""
    return date.today()


@pytest.fixture
def tomorrow() -> date:
    """Provide the tomorrow date."""
    return date.today() + timedelta(days=1)


@pytest.fixture
def later() -> date:
    """Provide the later date."""
    return date.today() + timedelta(days=2)


###################################################
# Data base
###################################################


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
