"""Repository interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .model import ProductProtocol


class RepositoryProtocol(Protocol):
    """Protocol for batch repository interface."""

    def add(self, product: ProductProtocol) -> None:
        """Add product."""

    def get(self, sku: str) -> ProductProtocol:
        """Get batch."""

    def list(self) -> list[ProductProtocol]:
        """Get batches."""
