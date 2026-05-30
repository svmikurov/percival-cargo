"""Domain model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    """Product order line.

    Parameters
    ----------
    order_id : str
        Order identifier.
    sku : `str`
        Stock-keeping unit of product.
    qty : `int`
        Product quantity in order.

    """

    order_id: str
    sku: str
    qty: int


class Batch:
    """Product batch.

    Parameters
    ----------
    ref : `str`
        Order reference.
    sku : `str`
        Stock-keeping unit of product.
    qty : `int`
        Product quantity.

    """

    def __init__(
        self,
        ref: str,
        sku: str,
        qty: int,
    ) -> None:
        """Construct the model."""
        self.ref = ref
        self.sku = sku
        self.qty = qty
        self.lines: set[OrderLine] = set()

    def allocate(self, line: OrderLine) -> None:
        """Allocate order line in batch."""
        if self.can_allocate(line):
            self.lines.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        """Check that product can be allocated."""
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def available_quantity(self) -> int:
        """Get available product quantity."""
        return self.qty - sum(line.qty for line in self.lines)
