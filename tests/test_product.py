"""Domain model Product tests."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pytest

from percival_cargo.domain import events
from percival_cargo.domain.model import Batch, OrderLine, Product

if TYPE_CHECKING:
    from percival_cargo import ports


@pytest.fixture
def today() -> date:
    return date.today()


@pytest.fixture
def batch(today: date) -> ports.BatchProtocol:
    return Batch(ref='reference-01', sku='TABLE', qty=10, eta=today)


@pytest.fixture
def line() -> ports.OrderLineProtocol:
    return OrderLine(order_id='order-01', sku='TABLE', qty=10)


@pytest.fixture
def other_line() -> ports.OrderLineProtocol:
    return OrderLine(order_id='order-02', sku='TABLE', qty=10)


@pytest.fixture
def product(batch: ports.BatchProtocol) -> ports.ProductProtocol:
    return Product(sku='TABLE', batches=[batch])


def test_records_out_of_stock_event_if_cannot_allocate(
    product: ports.ProductProtocol,
    line: ports.OrderLineProtocol,
    other_line: ports.OrderLineProtocol,
) -> None:
    # Arrange
    product.allocate(line)

    # Act
    allocation = product.allocate(other_line)
    assert product.events[-1] == events.OutOfStock(sku='TABLE')
    assert allocation is None
