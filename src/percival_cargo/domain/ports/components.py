"""Domain interface components."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from datetime import date

Event = TypeVar('Event')
OrderLine_contra = TypeVar('OrderLine_contra', contravariant=True)


###################################################
# Attributes
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


class HasEvents(Protocol[Event]):
    @property
    def events(self) -> list[Event]: ...


###################################################
# Methods
###################################################


class Allocatable(Protocol[OrderLine_contra]):
    def allocate(self, line: OrderLine_contra) -> str | None: ...


class DeAllocatable(Protocol[OrderLine_contra]):
    def deallocate(self, line: OrderLine_contra) -> None: ...


class CanAllocate(Protocol[OrderLine_contra]):
    def can_allocate(self, line: OrderLine_contra) -> bool: ...
