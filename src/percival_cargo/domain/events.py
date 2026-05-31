"""Domain events."""

from dataclasses import dataclass


class Event:
    """Event."""


@dataclass
class OutOfStock(Event):
    """out of stock event."""

    sku: str
