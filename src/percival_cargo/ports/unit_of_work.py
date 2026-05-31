"""Protocols for Unit Of Work interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Self

from . import repository

if TYPE_CHECKING:
    from . import components


class UnitOfWorkProtocol(
    components.HasProducts[repository.RepositoryProtocol],
    components.CanCommit,
    components.CanCollectNewEvents,
    components.CanRollback,
    Protocol,
):
    """Protocol fo Unit Of Work interface."""

    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...
