"""Fake repositories."""

from __future__ import annotations

from typing import TYPE_CHECKING

from percival_cargo.application.abstract import AbstractBatchUoW
from percival_cargo.domain import model as model
from percival_cargo.infrastructure.abstract import AbstractRepository

if TYPE_CHECKING:
    from percival_cargo.domain.protocols import BatchProtocol


class FakeBatchRepository(AbstractRepository):
    """Fake batch repository."""

    def __init__(self, batches: set[BatchProtocol]) -> None:
        self._batches = batches

    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""
        self._batches.add(batch)

    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[BatchProtocol]:
        """Get all batches."""
        return list(self._batches)


class FakeBatchUoW(AbstractBatchUoW):
    """Fake Batch UoW."""

    def __init__(self) -> None:
        self._repo = FakeBatchRepository(set())
        self._committed = False

    def commit(self) -> None:
        self.committed = True

    def _rollback(self) -> None:
        pass
