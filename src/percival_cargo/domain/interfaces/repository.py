"""Repository interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .model import BatchProtocol


class BatchRepositoryProtocol(Protocol):
    """Protocol for batch repository interface."""

    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""

    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""

    def list(self) -> list[BatchProtocol]:
        """Get batches."""
