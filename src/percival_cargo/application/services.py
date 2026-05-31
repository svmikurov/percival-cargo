"""Application services."""

from percival_cargo.domain import model
from percival_cargo.domain.ports.model import (
    BatchProtocol,
    OrderLineProtocol,
)
from percival_cargo.domain.ports.repository import RepositoryProtocol

from .exceptions import InvalidSku


def is_valid_sku(sku: str, batches: list[BatchProtocol]) -> bool:
    """Check is valid SKU."""
    return sku in {b.sku for b in batches}


def allocate(  # type: ignore
    line: OrderLineProtocol,
    repo: RepositoryProtocol,
    session,
) -> str:
    """Allocate."""
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Недопустимый артикул {line.sku}')

    batch_ref = model.allocate(line, batches)
    session.commit()
    return batch_ref
