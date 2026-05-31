"""Fake repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from .abstract import AbstractBatchRepository

if TYPE_CHECKING:
    from percival_cargo import ports


class FakeRepository(AbstractBatchRepository):
    """Fake repository."""

    def __init__(self, batches: list[ports.ProductProtocol]) -> None:
        """Construct the repository."""
        self._batches = set(batches)

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
        """Get all batches."""
        raise NotImplementedError
