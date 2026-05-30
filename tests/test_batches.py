"""Test batches."""

import pytest

from percival_cargo.domain.exceptions import OutOfBatch
from percival_cargo.domain.model import Batch, OrderLine

from .tools import make_batch_and_line


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
