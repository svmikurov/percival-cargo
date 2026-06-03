"""Domain layer service."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import model


def allocate(line: model.OrderLine, batches: list[model.Batch]) -> str:
    """Allocate order line in prefers batch."""
    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference
