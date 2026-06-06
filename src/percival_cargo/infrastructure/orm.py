"""ORM."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import registry

from percival_cargo.domain import model

mapper_registry = registry()
metadata = mapper_registry.metadata

order_lines = Table(
    'order_lines',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('order_id', String(255)),
)


def start_mappers() -> None:
    """Настройка маппинга (SQLAlchemy 2.0 style)."""
    mapper_registry.map_imperatively(model.OrderLine, order_lines)
