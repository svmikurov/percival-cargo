"""ORM configuration for SQLAlchemy 2.0.

This module sets up the mapping between domain models and database
tables using SQLAlchemy's imperative mapping pattern. This approach
keeps the domain models completely decoupled from the database
infrastructure.
"""

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import registry, relationship

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

# Database table definition for batches.
#
# This table stores product batches with their quantities and expected
# arrival dates. Each batch represents a shipment or stock batch
# that can be allocated to customer orders.
batches = Table(
    'batches',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column(
        'reference',
        String(255),
        unique=True,
        nullable=False,
        doc='Unique batch reference identifier',
    ),
    Column(
        'sku',
        String(255),
        nullable=False,
        doc='Stock keeping unit - product identifier',
    ),
    Column(
        '_purchased_quantity',
        Integer,
        nullable=False,
        doc='Initial quantity purchased (before allocations)',
    ),
    Column(
        'eta',
        Date,
        nullable=True,
        doc='Estimated time of arrival (None means in stock)',
    ),
)

# Association table for many-to-many relationship between batches and order lines.
# This table tracks which order lines are allocated to which batches.
allocations = Table(
    'allocations',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column(
        'orderline_id',
        ForeignKey('order_lines.id'),
        doc='Reference to allocated order line',
    ),
    Column(
        'batch_id',
        ForeignKey('batches.id'),
        doc='Reference to batch containing the allocation',
    ),
)


def start_mappers() -> None:
    """Set up ORM mapping between domain models and database tables.

    Configures SQLAlchemy to map domain models to database tables using
    imperative mapping pattern.

    Why imperative mapping?
        - Domain models stay pure (no SQLAlchemy dependencies)
        - Follows Clean Architecture / DDD principles
        - Models can be tested without database setup
        - Full control over mapping configuration

    What happens after calling this function?
        1. SQLAlchemy creates internal Mapper objects for OrderLine and Batch
        2. The mappers know which tables to use for persistence
        3. Session operations (add, query, delete) work with domain objects
        4. SQLAlchemy automatically converts between objects and rows
        5. Relationship between Batch and OrderLine is configured

    Mappings configured:
        - OrderLine -> order_lines table
        - Batch -> batches table
        - Batch._allocations -> many-to-many relationship via allocations table

    Example:
        >>> from percival_cargo.infrastructure.orm_sqlachemy import start_mappers
        >>> from percival_cargo.domain import model
        >>> from sqlalchemy import create_engine
        >>> from sqlalchemy.orm import Session
        >>>
        >>> # Setup (call once at application startup)
        >>> start_mappers()
        >>> engine = create_engine('sqlite:///app.db')
        >>> metadata.create_all(engine)
        >>>
        >>> # Usage
        >>> session = Session(bind=engine)
        >>> batch = model.Batch("BATCH-001", "CHAIR", 100, eta=None)
        >>> line = model.OrderLine("ORD-001", "CHAIR", 2)
        >>> batch.allocate(line)
        >>> session.add(batch)
        >>> session.commit()

    Important:
        This function should be called exactly once during application
        initialization, before any database operations are performed.
        Calling it multiple times will raise an ArgumentError because
        classes would be mapped twice.

    Raises:
        sqlalchemy.exc.ArgumentError: If any class has already been mapped.

    """
    # Map OrderLine domain model to order_lines table
    order_line_mapper = mapper_registry.map_imperatively(
        model.OrderLine,
        order_lines,
    )

    # Map Batch domain model to batches table with relationship to OrderLine
    # The _allocations property is configured as a many-to-many relationship
    # using the allocations association table.
    mapper_registry.map_imperatively(
        model.Batch,
        batches,  # ✅ Исправлено: используем правильную таблицу
        properties={
            '_sku': batches.c.sku,
            '_eta': batches.c.eta,
            # Relationship
            '_allocations': relationship(
                order_line_mapper,  # Use the mapper, not the class
                secondary=allocations,
                collection_class=set,
            ),
        },
    )
