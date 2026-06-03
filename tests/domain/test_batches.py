"""Test the batches."""

import pytest

from percival_cargo.domain.model import Batch, OrderLine

SMALL_QUANTITY = 2
LARGE_QUANTITY = 20


def test_allocating_to_a_batch_reduces_the_available_quantity() -> None:
    # Arrange
    line = OrderLine('order-01', 'TABLE', SMALL_QUANTITY)
    batch = Batch('ref-01', 'TABLE', LARGE_QUANTITY, None)

    # Act
    batch.allocate(line)

    # Assert
    assert batch.available_quantity == LARGE_QUANTITY - SMALL_QUANTITY


def test_can_only_deallocate_allocated_lines() -> None:
    line = OrderLine('order-01', 'TABLE', SMALL_QUANTITY)
    batch = Batch('ref-01', 'TABLE', LARGE_QUANTITY, None)

    # Act
    batch.deallocate(line)

    # Assert
    assert batch.available_quantity == LARGE_QUANTITY


def test_allocation_is_idempotent() -> None:
    # Arrange
    line = OrderLine('order-01', 'TABLE', SMALL_QUANTITY)
    batch = Batch('ref-01', 'TABLE', LARGE_QUANTITY, None)

    # Act
    batch.allocate(line)
    batch.allocate(line)

    # Assert
    assert batch.available_quantity == LARGE_QUANTITY - SMALL_QUANTITY


class TestCanAllocate:
    @pytest.mark.parametrize(
        'line_qty, batch_qty, expected',
        (
            (SMALL_QUANTITY, LARGE_QUANTITY, True),
            (LARGE_QUANTITY, LARGE_QUANTITY, True),
            (LARGE_QUANTITY, SMALL_QUANTITY, False),
        ),
    )
    def test_can_allocate_if_available_greater_than_required(
        self,
        line_qty: int,
        batch_qty: int,
        expected: bool,
    ) -> None:
        # Arrange
        line = OrderLine('order-id', 'TABLE', line_qty)
        batch = Batch('reference-id', 'TABLE', batch_qty, None)

        # Act & Assert
        assert batch.can_allocate(line) is expected

    def test_cannot_allocate_if_skus_do_not_match(self) -> None:
        # Arrange
        line = OrderLine('order-01', 'TABLE', SMALL_QUANTITY)
        batch = Batch('ref-01', 'CHAIR', LARGE_QUANTITY, None)

        # Act & Assert
        assert batch.can_allocate(line) is False
