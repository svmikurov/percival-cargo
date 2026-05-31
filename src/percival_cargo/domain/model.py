"""Domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from . import events
from .exceptions import OutOfBatchException, OutOfStockException

if TYPE_CHECKING:
    from datetime import date

    from .ports.model import (
        BatchProtocol,
        EventProtocol,
        OrderLineProtocol,
    )


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
            raise OutOfBatchException from err

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

    def __gt__(self, other: BatchProtocol) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


class Product:
    """Product."""

    def __init__(
        self,
        sku: str,
        batches: list[BatchProtocol],
        version_number: int = 0,
    ) -> None:
        """Construct the model."""
        self._sku = sku
        self._batches = batches
        self._version_number = version_number
        self._events: list[EventProtocol] = []

    def allocate(self, line: OrderLineProtocol) -> str | None:
        """Allocate."""
        try:
            batch = next(
                b for b in sorted(self._batches) if b.can_allocate(line)
            )
        except StopIteration:
            self._events.append(events.OutOfStock(line.sku))
            return None

        batch.allocate(line)
        self._version_number += 1
        return batch.reference

    @property
    def events(self) -> list[EventProtocol]:
        """Get events."""
        return self._events


def allocate(line: OrderLineProtocol, batches: list[BatchProtocol]) -> str:
    """Allocate the order line to faster batch."""
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
    except StopIteration as err:
        raise OutOfStockException(
            f'The item {line.sku} is out of stock'
        ) from err
    batch.allocate(line)
    return batch.reference
