"""Domain model interface."""

from __future__ import annotations

from typing import Protocol

###################################################
# Components
###################################################


class HasOrderID(Protocol):
    @property
    def order_id(self) -> str: ...


class HasSKU(Protocol):
    @property
    def sku(self) -> str: ...


class HasQuantity(Protocol):
    @property
    def qty(self) -> int: ...


class HasAvailableQuantity(Protocol):
    @property
    def available_quantity(self) -> int: ...


class Allocatable(Protocol):
    def allocate(self, line: OrderLineProtocol) -> None: ...


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
    Allocatable,
    CanAllocate,
    DeAllocatable,
    HasAvailableQuantity,
    Protocol,
):
    """Protocol for product batch interface."""
