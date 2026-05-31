"""Domain event interface."""

from typing import Protocol

from . import components


class EventProtocol(Protocol):
    """Protocol for event general interface."""


class BatchCreatedProtocol(
    components.HasReference,
    components.HasSKU,
    components.HasQuantity,
    components.HasETA,
    EventProtocol,
    Protocol,
):
    """Protocol for batch created event interface."""


class AllocationRequiredProtocol(
    components.HasOrderID,
    components.HasSKU,
    components.HasQuantity,
    EventProtocol,
    Protocol,
):
    """Protocol for allocation required event interface."""


class OutOfStock(
    components.HasSKU,
    EventProtocol,
    Protocol,
):
    """Protocol for out of stock SKU event interface."""
