"""Repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from percival_cargo.domain import model

from .abstract import AbstractRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from percival_cargo.domain.protocols import BatchProtocol


class SqlAlchemyRepository(AbstractRepository):
    """SqlAlchemy repository."""

    def __init__(self, session: Session) -> None:
        """Construct the repository."""
        self._session = session

    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""
        self._session.add(batch)

    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""
        return (
            self._session.query(model.Batch)
            .filter_by(reference=reference)
            .one()
        )

    def list(self) -> list[BatchProtocol]:
        """Get all batches."""
        return self._session.query(model.Batch).all()  # type: ignore
