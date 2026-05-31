"""Test service."""

import pytest

from percival_cargo.application import exceptions, services
from percival_cargo.domain import model
from percival_cargo.domain.interfaces.repository import BatchRepositoryProtocol
from percival_cargo.infrastructure.repositories.impl_fake import FakeRepository


class FakeSession:
    committed = False

    def commit(self) -> None:
        self.committed = True


@pytest.fixture
def repo() -> BatchRepositoryProtocol:
    """Provide the repository."""
    batch = model.Batch('ref-01', 'CHAIR', qty=100, eta=None)
    repo = FakeRepository([batch])
    return repo


def test_returns_allocation(
    repo: BatchRepositoryProtocol,
) -> None:
    # Arrange
    line = model.OrderLine('order-01', 'CHAIR', 10)

    # Act
    result = services.allocate(line, repo, FakeSession())

    # Assert
    assert result == 'ref-01'


def test_error_for_invalid_sku(
    repo: BatchRepositoryProtocol,
) -> None:
    # Arrange
    line = model.OrderLine('order-02', 'NON_EXISTENT_SKU', 10)

    # Act & Assert
    with pytest.raises(
        exceptions.InvalidSku,
        match='Недопустимый артикул NON_EXISTENT_SKU',
    ):
        services.allocate(line, repo, FakeSession())


def test_commits(
    repo: BatchRepositoryProtocol,
) -> None:
    # Arrange
    line = model.OrderLine('order-03', 'CHAIR', 10)
    session = FakeSession()

    # Act
    services.allocate(line, repo, session)

    # Assert
    assert session.committed is True
