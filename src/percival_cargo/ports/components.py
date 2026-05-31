"""Domain interface components."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from datetime import date

Event = TypeVar('Event')

OrderLine_contra = TypeVar('OrderLine_contra', contravariant=True)
Batch = TypeVar('Batch')

Repository_cov = TypeVar('Repository_cov', covariant=True)


###################################################
# Attributes
###################################################


class HasOrderID(Protocol):
    @property
    def order_id(self) -> str: ...


class HasReference(Protocol):
    @property
    def ref(self) -> str: ...


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


class HasBatches(Protocol[Batch]):
    @property
    def batches(self) -> list[Batch]: ...


class HasProducts(Protocol[Repository_cov]):
    @property
    def products(self) -> Repository_cov: ...


###################################################
# Methods
###################################################


# REVIEW: Update option reference allocate result


class Allocatable(Protocol[OrderLine_contra]):
    def allocate(self, line: OrderLine_contra) -> None: ...


class CanAllocate(Protocol[OrderLine_contra]):
    def allocate(self, line: OrderLine_contra) -> str: ...


class OptionAllocatable(Protocol[OrderLine_contra]):
    def allocate(self, line: OrderLine_contra) -> str | None: ...


class IsCanAllocate(Protocol[OrderLine_contra]):
    def can_allocate(self, line: OrderLine_contra) -> bool: ...


class DeAllocatable(Protocol[OrderLine_contra]):
    def deallocate(self, line: OrderLine_contra) -> None: ...


class CanCommit(Protocol):
    def commit(self) -> None: ...


class CanCollectNewEvents(Protocol):
    def collect_new_events(self) -> None: ...


class CanRollback(Protocol):
    def rollback(self) -> None: ...
