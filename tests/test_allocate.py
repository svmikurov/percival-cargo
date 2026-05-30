"""Test the product order line allocation to batch."""

from datetime import date, timedelta

import pytest

from percival_cargo.domain.exceptions import OutOfStock
from percival_cargo.domain.model import Batch, OrderLine, allocate

today = date.today()
tomorrow = date.today() + timedelta(days=1)
later = date.today() + timedelta(days=2)


def test_prefers_current_stock_batches_to_shipments() -> None:
    # Arrange
    in_stock_batch = Batch('in_stock_batch', 'RETRO-CLOCK', 100, eta=None)
    in_ship_batch = Batch('in_ship_batch', 'RETRO-CLOCK', 100, eta=tomorrow)
    line = OrderLine('order-001', 'RETRO-CLOCK', 10)

    # Act
    allocate(line, [in_ship_batch, in_stock_batch])

    # Assert
    assert in_stock_batch.available_quantity == 90
    assert in_ship_batch.available_quantity == 100


def test_prefers_earlier_batches() -> None:
    # Arrange
    earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=today)
    medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=tomorrow)
    latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=later)
    line = OrderLine('order1', 'MINIMALIST-SPOON', 10)

    # Act
    allocate(line, [medium, earliest, latest])

    # Assert
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref() -> None:
    # Arrange
    in_stock_batch = Batch('in_stock_batch', 'RETRO-CLOCK', 100, eta=None)
    in_ship_batch = Batch('in_ship_batch', 'RETRO-CLOCK', 100, eta=tomorrow)
    line = OrderLine('order-001', 'RETRO-CLOCK', 10)

    # Act
    reference = allocate(line, [in_ship_batch, in_stock_batch])

    # Assert
    isinstance(reference, int)


def test_raises_out_of_stock_exception_if_cannot_allocate() -> None:
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    line1 = OrderLine('order1', 'SMALL-FORK', 10)
    line2 = OrderLine('order2', 'SMALL-FORK', 1)
    allocate(line1, [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(line2, [batch])
