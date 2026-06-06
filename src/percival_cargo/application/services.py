"""Application layer services."""

from __future__ import annotations

from typing import TYPE_CHECKING

from percival_cargo.domain import services as domain_services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from percival_cargo.domain.protocols import (
        BatchProtocol,
        BatchRepositoryProtocol,
        OrderLineProtocol,
    )


class InvalidSku(Exception):
    """Raises then passed to batch the invalid order line."""

    pass


def is_valid_sku(sku: str, batches: list[BatchProtocol]) -> bool:
    """Check that SKU is valid."""
    return sku in {b.sku for b in batches}


def allocate(
    line: OrderLineProtocol,
    repo: BatchRepositoryProtocol,
    session: Session,
) -> str:
    """Allocate the order line to batch."""
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Недопустимый артикул {line.sku}')

    batch_ref = domain_services.allocate(line, batches)
    session.commit()
    return batch_ref
