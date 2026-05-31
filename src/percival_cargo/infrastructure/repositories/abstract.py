"""Abstract base class for repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from percival_cargo.ports.repository import RepositoryProtocol

if TYPE_CHECKING:
    from percival_cargo.ports.model import ProductProtocol


class AbstractBatchRepository(ABC, RepositoryProtocol):
    """ABC for batch repository."""

    @override
    @abstractmethod
    def add(self, product: ProductProtocol) -> None:
        """Add batch."""

    @override
    @abstractmethod
    def get(self, sku: str) -> ProductProtocol:
        """Get batch."""

    @override
    @abstractmethod
    def list(self) -> list[ProductProtocol]:
        """Get batches."""
