"""SqlAlchemy repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from percival_cargo.domain.model import Batch

from .abstract import AbstractBatchRepository

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session

    from percival_cargo.domain.interfaces.model import BatchProtocol


class SqlAlchemyBatchRepository(AbstractBatchRepository):
    """SqlAlchemy batch repository."""

    def __init__(self, session: Session) -> None:
        """Construct the repository."""
        self._session = session

    @override
    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""
        self._session.add(batch)

    @override
    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""
        return self._session.query(Batch).filter_by(reference=reference).one()

    @override
    def list(self) -> list[BatchProtocol]:
        """Get batches."""
        return list(self._session.query(Batch).all())
