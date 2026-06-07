"""Repository tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy import text

from percival_cargo.domain import model
from percival_cargo.infrastructure import repository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from percival_cargo.domain.protocols import (
        BatchProtocol,
        BatchRepositoryProtocol,
    )


@pytest.fixture
def batch() -> BatchProtocol:
    return model.Batch('batch1', 'RUSTY-SOAP_DISH', 100, eta=None)


@pytest.fixture
def repo(session: Session) -> BatchRepositoryProtocol:
    return repository.SqlAlchemyRepository(session)


def test_repository_can_save_a_batch(
    repo: BatchRepositoryProtocol,
    session: Session,
) -> None:
    # Arrange
    attrs = ('batch1', 'RUSTY-SOAP_DISH', 100, None)
    batch = model.Batch(*attrs)
    expected = [attrs]

    # Act
    repo.add(batch)
    session.commit()

    # Assert
    rows = list(
        session.execute(
            text(
                'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
            )
        )
    )
    assert rows == expected
