"""Abstract base class for repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence, override

from percival_cargo.domain.interfaces.repository import BatchRepositoryProtocol

if TYPE_CHECKING:
    from percival_cargo.domain.interfaces.model import BatchProtocol


class AbstractBatchRepository(ABC, BatchRepositoryProtocol):
    """ABC for batch repository."""

    @override
    @abstractmethod
    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""

    @override
    @abstractmethod
    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""

    @override
    @abstractmethod
    def list(self) -> Sequence[BatchProtocol]:
        """Get batches."""
