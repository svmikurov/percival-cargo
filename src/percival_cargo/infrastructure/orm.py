"""ORM configuration for SQLAlchemy 2.0.

This module sets up the mapping between domain models and database
tables using SQLAlchemy's imperative mapping pattern. This approach
keeps the domain models completely decoupled from the database
infrastructure.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import registry

from percival_cargo.domain import model

# Registry container that holds all mappers and provides configuration
# for both classical and declarative mapping patterns.
#
# The registry is the central object for:
#   - Tracking all mapped classes
#   - Managing metadata (Table objects)
#   - Configuring relationships between entities
mapper_registry = registry()

# Collection of all Table objects associated with this registry.
#
# This metadata object is used for:
#   - Creating database schema: metadata.create_all(engine)
#   - Dropping database schema: metadata.drop_all(engine)
#   - Reflecting existing database schema
metadata = mapper_registry.metadata

# Database table definition for order lines.
#
# This table stores individual items within purchase orders.
# Each record represents a single product in a customer's order.
order_lines = Table(
    'order_lines',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255), doc='Stock keeping unit - product identifier'),
    Column('qty', Integer, nullable=False, doc='Quantity of items ordered'),
    Column('order_id', String(255), doc='Parent order identifier'),
)


def start_mappers() -> None:
    """Set up ORM mapping between domain models and database tables.

    Configures SQLAlchemy to map the OrderLine domain model to the
    order_lines database table using imperative mapping.

    Why imperative mapping?
        - Domain models stay pure (no SQLAlchemy dependencies)
        - Follows Clean Architecture / DDD principles
        - Models can be tested without database setup
        - Full control over mapping configuration

    What happens after calling this function?
        1. SQLAlchemy creates an internal Mapper object for OrderLine
        2. The mapper knows which table to use for persistence
        3. Session operations (add, query, delete) work with OrderLine
        4. SQLAlchemy automatically converts between objects and rows
    """
    mapper_registry.map_imperatively(model.OrderLine, order_lines)
