"""Test application services."""

import pytest

from percival_cargo.application import services
from percival_cargo.domain import model
from tests.fake.repository import FakeBatchRepository


class FakeSession:
    committed = False

    def commit(self) -> None:
        self.committed = True


def test_returns_allocation() -> None:
    # Arrange
    line = model.OrderLine('o1', 'COMPLICATED-LAMP', 10)
    batch = model.Batch('b1', 'COMPLICATED-LAMP', 100, eta=None)
    repo = FakeBatchRepository(set([batch]))

    # Act
    result = services.allocate(line, repo, FakeSession())  # type: ignore

    # Assert
    assert result == 'b1'


def test_error_for_invalid_sku() -> None:
    # Arrange
    line = model.OrderLine('o1', 'NON_EXISTENT_SKU', 10)
    batch = model.Batch('b1', 'AREAL_SKU', 100, eta=None)
    repo = FakeBatchRepository(set([batch]))

    # Act & Assert
    with pytest.raises(
        services.InvalidSku, match='Недопустимый артикул NON_EXISTENT_SKU'
    ):
        services.allocate(line, repo, FakeSession())  # type: ignore


def test_commits() -> None:
    # Arrange
    line = model.OrderLine('o1', 'OMINOUS-MIRROR', 10)
    batch = model.Batch('b1', 'OMINOUS-MIRROR', 100, eta=None)
    repo = FakeBatchRepository(set([batch]))
    session = FakeSession()

    # Act
    services.allocate(line, repo, session)  # type: ignore

    # Assert
    assert session.committed is True
