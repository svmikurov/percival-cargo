"""Test tools."""

from percival_cargo.domain.model import Batch, OrderLine


def make_batch_and_line(
    squ: str,
    batch_qty: int,
    line_qty: int,
) -> tuple[Batch, OrderLine]:
    """Create the product order line and batch."""
    return (
        Batch('batch-001', squ, batch_qty),
        OrderLine('order-001', squ, line_qty),
    )
