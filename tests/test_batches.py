"""Test batches."""

import pytest

from percival_cargo.domain.exceptions import OutOfBatch

from .tools import make_batch_and_line


def test_can_only_deallocate_allocated_lines() -> None:
    # Arrange
    batch, unlocated_line = make_batch_and_line('CHAIR-RED', 20, 2)

    # Act
    with pytest.raises(OutOfBatch):
        batch.deallocate(unlocated_line)

    # Assert
    assert batch.available_quantity == 20
