"""Test batches."""

import pytest

from percival_cargo.domain.exceptions import OutOfBatch
from percival_cargo.domain.model import Batch, OrderLine

from .tools import make_batch_and_line


@pytest.mark.parametrize(
    'squ, batch_qty, line_qty, expected_qty',
    (
        ('TABLE-SMALL', 20, 2, 18),
        ('TABLE-SMALL', 2, 20, 2),
        ('TABLE-SMALL', 20, 20, 0),
    ),
)
def test_allocation(
    squ: str,
    batch_qty: int,
    line_qty: int,
    expected_qty: bool,
) -> None:
    """Test the product order line allocation to batch."""
    # Arrange
    batch, line = make_batch_and_line(squ, batch_qty, line_qty)

    # Act
    batch.allocate(line)

    # Assert
    assert batch.available_quantity == expected_qty


def test_the_duplicate_allocation() -> None:
    """Test that the duplicate allocation not available."""
    # Arrange
    batch_qty = 20
    line_qty = 2
    expected_qty = batch_qty - line_qty

    batch, line = make_batch_and_line('TABLE-SMALL', batch_qty, line_qty)

    # Act
    batch.allocate(line)
    batch.allocate(line)

    # Assert
    assert batch.available_quantity == expected_qty


def test_the_different_allocation() -> None:
    """Test that the different allocations is available."""
    # Arrange
    batch_qty = 20
    line_qty = 2
    other_line_qty = 2
    expected_qty = batch_qty - line_qty - other_line_qty

    batch, line = make_batch_and_line('TABLE-SMALL', batch_qty, line_qty)
    other_line = OrderLine('order-002', 'TABLE-SMALL', line_qty)

    # Act
    batch.allocate(line)
    batch.allocate(other_line)

    # Assert
    assert batch.available_quantity == expected_qty


def test_the_different_line_and_batch() -> None:
    """Test that cannot allocate if SKUs do not match."""
    # Arrange
    batch_qty = 20
    line_qty = 2

    batch = Batch('batch-001', 'TABLE-BIG', batch_qty, eta=None)
    line = OrderLine('order-001', 'TABLE-SMALL', line_qty)

    # Act
    batch.allocate(line)

    # Assert
    assert batch.available_quantity == batch_qty


def test_can_only_deallocate_allocated_lines() -> None:
    # Arrange
    batch, unlocated_line = make_batch_and_line('CHAIR-RED', 20, 2)

    # Act
    with pytest.raises(OutOfBatch):
        batch.deallocate(unlocated_line)

    # Assert
    assert batch.available_quantity == 20


def test_can_allocate_if_available_greater_than_required() -> None:
    large_batch, small_line = make_batch_and_line('ELEGANT-LAMP', 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required() -> None:
    small_batch, large_line = make_batch_and_line('ELEGANT-LAMP', 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required() -> None:
    batch, line = make_batch_and_line('ELEGANT-LAMP', 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match() -> None:
    batch = Batch('batch-001', 'UNCOMFORTABLE-CHAIR', 100, eta=None)
    different_sku_line = OrderLine('order-123', 'EXPENSIVE-TOASTER', 10)
    assert batch.can_allocate(different_sku_line) is False
