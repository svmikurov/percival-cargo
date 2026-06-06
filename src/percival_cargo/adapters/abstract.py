"""Abstract base classes for domain interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from percival_cargo.domain.protocols import BatchProtocol


class AbstractRepository(ABC):
    """Protocol for repository interface."""

    @abstractmethod
    def add(self, batch: BatchProtocol) -> None:
        """Add batch."""

    @abstractmethod
    def get(self, reference: str) -> BatchProtocol:
        """Get batch."""
