"""Abstract base classes for domain interfaces."""

from abc import ABC, abstractmethod

from . import model


class AbstractRepository(ABC):
    """Protocol for repository interface."""

    @abstractmethod
    def add(self, batch: model.Batch) -> None:
        """Add batch."""

    @abstractmethod
    def get(self, reference: str) -> model.Batch:
        """Get batch."""
