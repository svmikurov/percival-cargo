"""Domain events."""

from dataclasses import dataclass
from datetime import date


class Event:
    """Event."""


@dataclass
class OutOfStock(Event):
    """out of stock event."""

    sku: str


@dataclass
class BatchCreated(Event):
    """Batch created event."""

    ref: str
    sku: str
    qty: int
    eta: date | None = None


@dataclass
class AllocationRequired(Event):
    """Allocation required event."""

    order_id: str
    sku: str
    qty: str
