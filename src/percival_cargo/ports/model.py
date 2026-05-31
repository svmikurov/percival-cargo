"""Domain model interface."""

from typing import Protocol

from . import components


class EventProtocol(Protocol):
    """Protocol for event interface."""


class OrderLineProtocol(
    components.HasOrderID,
    components.HasSKU,
    components.HasQuantity,
    Protocol,
):
    """Protocol for order line interface."""


class BatchProtocol(
    components.HasReference,
    components.HasSKU,
    components.HasETA,
    components.Allocatable[OrderLineProtocol],
    components.IsCanAllocate[OrderLineProtocol],
    components.DeAllocatable[OrderLineProtocol],
    components.HasAvailableQuantity,
    Protocol,
):
    """Protocol for batch interface."""

    def __gt__(self, other: 'BatchProtocol') -> bool: ...
    def __eq__(self, other: object) -> bool: ...


class ProductProtocol(
    components.HasEvents[EventProtocol],
    components.HasBatches[BatchProtocol],
    components.OptionAllocatable[OrderLineProtocol],
    Protocol,
):
    """Protocol for product interface."""
