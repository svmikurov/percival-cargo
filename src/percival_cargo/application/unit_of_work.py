"""Unit Of Work."""

from typing import Callable

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from percival_cargo import config
from percival_cargo.infrastructure import repository

from .abstract import AbstractBatchUoW

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_url(),
    )
)


class SqlAlchemyBatchUoW(AbstractBatchUoW):
    """SqlAlchemy Batch repository UoW."""

    def __init__(
        self,
        session_factory: Callable[[], Session] = DEFAULT_SESSION_FACTORY,
    ) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory()
        self._repo = repository.SqlAlchemyRepository(self._session)
        return super().__enter__()

    def __exit__(self, *args: object) -> None:
        super().__exit__(*args)
        self._session.close()

    def commit(self) -> None:
        """Commit."""
        self._session.commit()

    def _rollback(self) -> None:
        self._session.rollback()
