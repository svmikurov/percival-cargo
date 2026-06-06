"""Domain layer service tests."""

from datetime import date

from percival_cargo.domain import model, services

BATCH_QUANTITY = 20
ORDER_QUANTITY = 2
UPDATED_QUANTITY = BATCH_QUANTITY - ORDER_QUANTITY


def test_prefers_current_stock_batches_to_shipments(
    tomorrow: date,
) -> None:
    # Arrange
    in_stock_batch = model.Batch('in-stock', 'CHAIR', BATCH_QUANTITY, eta=None)
    shipment_batch = model.Batch(
        'shipment-batch', 'CHAIR', BATCH_QUANTITY, eta=tomorrow
    )
    line = model.OrderLine('order-01', 'CHAIR', ORDER_QUANTITY)

    # Act
    services.allocate(line, batches=[in_stock_batch, shipment_batch])

    # Assert
    assert in_stock_batch.available_quantity == UPDATED_QUANTITY
    assert shipment_batch.available_quantity == BATCH_QUANTITY


def test_prefers_earlier_batches(
    today: date,
    tomorrow: date,
    later: date,
) -> None:
    # Arrange
    earliest = model.Batch('speedy-batch', 'CHAIR', BATCH_QUANTITY, eta=today)
    medium = model.Batch('normal-batch', 'CHAIR', BATCH_QUANTITY, eta=tomorrow)
    latest = model.Batch('slow-batch', 'CHAIR', BATCH_QUANTITY, eta=later)
    line = model.OrderLine('order-01', 'CHAIR', ORDER_QUANTITY)

    # Act
    services.allocate(line, batches=[earliest, medium, latest])

    # Assert
    assert earliest.available_quantity == UPDATED_QUANTITY
    assert medium.available_quantity == BATCH_QUANTITY
    assert latest.available_quantity == BATCH_QUANTITY


def test_returns_allocated_batch_ref(
    tomorrow: date,
) -> None:
    in_stock_batch = model.Batch('in-stock', 'CHAIR', BATCH_QUANTITY, eta=None)
    shipment_batch = model.Batch(
        'shipment-batch', 'CHAIR', BATCH_QUANTITY, eta=tomorrow
    )
    line = model.OrderLine('order-01', 'CHAIR', ORDER_QUANTITY)

    # Act
    allocation = services.allocate(line, [in_stock_batch, shipment_batch])

    # Assert
    assert allocation == in_stock_batch._reference
