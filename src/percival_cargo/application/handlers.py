"""Application layer handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from percival_cargo.domain import model
from percival_cargo.domain.exceptions import InvalidSkuException
from percival_cargo.infrastructure import email

if TYPE_CHECKING:
    from percival_cargo.domain.ports import events, uow


def add_batch(
    event: events.BatchCreatedProtocol,
    uow: uow.UnitOfWorkProtocol,
) -> None:
    """Add batch."""
    with uow:
        product = uow.products.get(sku=event.sku)
        if not product:
            product = model.Product(event.sku, batches=[])
            uow.products.add(product)

        product.batches.append(
            model.Batch(event.ref, event.sku, event.qty, event.eta)
        )

        uow.commit()


def allocate(
    event: events.AllocationRequiredProtocol,
    uow: uow.UnitOfWorkProtocol,
) -> str | None:
    """Allocate."""
    line = model.OrderLine(event.order_id, event.sku, event.qty)

    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSkuException(f'Invalid sku {line.sku}')

        batch_ref = product.allocate(line)
        uow.commit()
        return batch_ref


def send_out_of_stock_notification(
    event: events.OutOfStock,
    uow: uow.UnitOfWorkProtocol,
) -> None:
    """Send out of stock notification."""
    email.send(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
