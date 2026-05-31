"""SqlAlchemy repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from .abstract import AbstractBatchRepository

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session

    from percival_cargo import ports


class SqlAlchemyBatchRepository(AbstractBatchRepository):
    """SqlAlchemy batch repository."""

    def __init__(self, session: Session) -> None:
        """Construct the repository."""
        self._session = session

    @override
    def add(self, product: ports.ProductProtocol) -> None:
        """Add batch."""
        raise NotImplementedError

    @override
    def get(self, sku: str) -> ports.ProductProtocol:
        """Get batch."""
        raise NotImplementedError

    @override
    def list(self) -> list[ports.ProductProtocol]:
        """Get batches."""
        raise NotImplementedError
