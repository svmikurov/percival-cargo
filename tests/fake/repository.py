"""Fake repositories."""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

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

    def list(self) -> Sequence[BatchProtocol]:
        """Get all batches."""
        return list(self._batches)
