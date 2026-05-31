"""Fake repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from .abstract import AbstractBatchRepository

if TYPE_CHECKING:
    from percival_cargo.domain.interfaces.model import BatchProtocol


class FakeRepository(AbstractBatchRepository):
    """Fake repository."""

    def __init__(self, batches: list[BatchProtocol]) -> None:
        """Construct the repository."""
        self._batches = set(batches)

    @override
    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""
        self._batches.add(batch)

    @override
    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""
        return next(b for b in self._batches if b.reference == reference)

    @override
    def list(self) -> list[BatchProtocol]:
        """Get all batches."""
        return list(self._batches)
