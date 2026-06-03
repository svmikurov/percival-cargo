"""Domain models."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    """Item order line."""

    order_id: str
    sku: str
    qty: int


class Batch:
    """Batch."""

    def __init__(
        self,
        ref: str,
        sku: str,
        qty: int,
        eta: date | None,
    ) -> None:
        """Construct the batch."""
        self.reference = ref
        self._sku = sku
        self._eta = eta
        self._purchased_quantity = qty
        self._allocations: set[OrderLine] = set()

    def allocate(self, line: OrderLine) -> None:
        """Allocate the line order to batch."""
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        """Deallocate the line order from batch."""
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        """Get allocated quantity."""
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        """Get available quantity."""
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        """Check that batch can allocate the line order."""
        return self._sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other: object) -> bool:
        """Check is equal."""
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __hash__(self) -> int:
        """Hash the batch."""
        return hash(self.reference)

    def __gt__(self, other: 'Batch') -> bool:
        """Check is greeter instance that other."""
        if self._eta is None:
            return False
        if other._eta is None:
            return True
        return self._eta > other._eta
