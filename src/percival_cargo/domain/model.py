"""Domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exceptions import OutOfBatch, OutOfStock

if TYPE_CHECKING:
    from datetime import date

    from .interfaces.model import OrderLineProtocol


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
    eta : date | None
        Estimated arrival time

    """

    def __init__(
        self,
        ref: str,
        sku: str,
        qty: int,
        eta: date | None,
    ) -> None:
        """Construct the model."""
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: set[OrderLineProtocol] = set()

    def allocate(self, line: OrderLineProtocol) -> None:
        """Allocate order line in batch."""
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLineProtocol) -> None:
        """Deallocate the order line from batch."""
        try:
            self._allocations.remove(line)
        except KeyError as err:
            raise OutOfBatch from err

    @property
    def allocated_quantity(self) -> int:
        """Get allocated product quantity."""
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        """Get available product quantity."""
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLineProtocol) -> bool:
        """Check that product can be allocated."""
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: Batch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    """Allocate the order line to faster batch."""
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
    except StopIteration as err:
        raise OutOfStock(f'The item {line.sku} is out of stock') from err
    batch.allocate(line)
    return batch.reference
