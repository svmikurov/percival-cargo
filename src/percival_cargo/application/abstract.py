"""Abstract base classes for application layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from percival_cargo.domain.protocols import BatchRepositoryProtocol


class AbstractBatchUoW(ABC):
    _repo: BatchRepositoryProtocol

    @property
    def repo(self) -> BatchRepositoryProtocol:
        return self._repo

    def __enter__(self) -> None: ...  # noqa: B027

    def __exit__(self, *args: object) -> None:
        self._rollback()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def _rollback(self) -> None: ...
