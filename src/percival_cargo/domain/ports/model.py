"""Domain model interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from datetime import date


###################################################
# Components
###################################################


class HasOrderID(Protocol):
    @property
    def order_id(self) -> str: ...


class HasReference(Protocol):
    @property
    def reference(self) -> str: ...


class HasSKU(Protocol):
    @property
    def sku(self) -> str: ...


class HasQuantity(Protocol):
    @property
    def qty(self) -> int: ...


class HasETA(Protocol):
    @property
    def eta(self) -> date | None: ...


class HasAvailableQuantity(Protocol):
    @property
    def available_quantity(self) -> int: ...


class HasEvents(Protocol):
    @property
    def events(self) -> list[EventProtocol]: ...


class Allocatable(Protocol):
    def allocate(self, line: OrderLineProtocol) -> str | None: ...


class DeAllocatable(Protocol):
    def deallocate(self, line: OrderLineProtocol) -> None: ...


class CanAllocate(Protocol):
    def can_allocate(self, line: OrderLineProtocol) -> bool: ...


###################################################
# Compositions
###################################################


class OrderLineProtocol(
    HasOrderID,
    HasSKU,
    HasQuantity,
    Protocol,
):
    """Protocol for order line interface."""


class BatchProtocol(
    HasReference,
    HasSKU,
    HasETA,
    Allocatable,
    CanAllocate,
    DeAllocatable,
    HasAvailableQuantity,
    Protocol,
):
    """Protocol for batch interface."""

    def __gt__(self, other: BatchProtocol) -> bool: ...
    def __eq__(self, other: object) -> bool: ...


class ProductProtocol(
    HasEvents,
    Allocatable,
    Protocol,
):
    """Protocol for product interface."""


class EventProtocol(Protocol):
    """Protocol for event interface."""
