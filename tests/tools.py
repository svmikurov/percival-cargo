"""Test tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from percival_cargo.domain.model import Batch, OrderLine

if TYPE_CHECKING:
    from percival_cargo.domain.interfaces.model import (
        BatchProtocol,
        OrderLineProtocol,
    )


def make_batch_and_line(
    squ: str,
    batch_qty: int,
    line_qty: int,
) -> tuple[BatchProtocol, OrderLineProtocol]:
    """Create the product order line and batch."""
    return (
        Batch('batch-001', squ, batch_qty, eta=None),
        OrderLine('order-001', squ, line_qty),
    )
