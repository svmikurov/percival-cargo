"""Domain layer service."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .protocols import BatchProtocol, OrderLineProtocol


def allocate(line: OrderLineProtocol, batches: list[BatchProtocol]) -> str:
    """Allocate order line in prefers batch."""
    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference
