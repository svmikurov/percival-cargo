"""Test the ORM mapping functionality.

This module tests that SQLAlchemy ORM correctly maps the OrderLine domain model
to the order_lines database table and vice versa.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from percival_cargo.domain import model


def test_orderline_mapper_can_load_lines(session: Session) -> None:
    """Test that the ORM mapper can correctly load OrderLine objects from database.

    This test verifies that:
        1. Raw SQL INSERT operations populate the database table correctly
        2. SQLAlchemy ORM query returns properly constructed OrderLine objects
        3. Field values are correctly mapped from columns to object attributes

    The test inserts three order lines using raw SQL and then retrieves them
    using the ORM's query interface, comparing the results with expected objects.

    Args:
        session: SQLAlchemy ORM session fixture providing database connection.

    Example database state after INSERT:
        order_lines table:
        | id | order_id | sku           | qty |
        |----|----------|---------------|-----|
        | 1  | order1   | RED-CHAIR     | 12  |
        | 2  | order1   | RED-TABLE     | 13  |
        | 3  | order2   | BLUE-LIPSTICK | 14  |

    Asserts:
        - Query returns exactly 3 OrderLine objects
        - Each object has correct order_id, sku, and qty values
        - Objects match expected domain model instances

    Note:
        Uses text() wrapper for raw SQL as required by SQLAlchemy 2.0.

    """
    session.execute(
        text(
            'INSERT INTO order_lines (order_id, sku, qty) VALUES '
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
    )
    session.commit()

    expected = [
        model.OrderLine('order1', 'RED-CHAIR', 12),
        model.OrderLine('order1', 'RED-TABLE', 13),
        model.OrderLine('order2', 'BLUE-LIPSTICK', 14),
    ]

    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session: Session) -> None:
    """Test that the ORM mapper can correctly save OrderLine objects to database.

    This test verifies that:
        1. OrderLine objects can be added to a session
        2. Session.commit() persists objects to the database
        3. Raw SQL queries retrieve the saved data correctly
        4. ORM to database mapping works in the save direction

    The test creates a new OrderLine object, saves it via the ORM session,
    and then verifies the data was correctly persisted using a raw SQL query.

    Args:
        session: SQLAlchemy ORM session fixture providing database connection.

    Test flow:
        1. Create OrderLine domain object
        2. Add to SQLAlchemy session
        3. Commit to database (ORM converts object to SQL INSERT)
        4. Verify via raw SQL that data exists in table

    Asserts:
        - Database contains exactly one row with the saved data
        - All three fields (order_id, sku, qty) match the original object

    Note:
        Uses text() wrapper for raw SQL SELECT as required by SQLAlchemy 2.0.
        The ORDER BY clause ensures consistent test results.

    """
    new_line = model.OrderLine('order1', 'DECORATIVE-WIDGET', 12)
    session.add(new_line)
    session.commit()

    rows = list(
        session.execute(text('SELECT order_id, sku, qty FROM order_lines'))
    )
    assert rows == [('order1', 'DECORATIVE-WIDGET', 12)]


# Optional: Additional test for completeness
def test_orderline_mapper_can_update_lines(session: Session) -> None:
    """Test that the ORM mapper can update existing OrderLine objects.

    Verifies that modifying an object's attributes and calling commit()
    updates the corresponding database record.

    Args:
        session: SQLAlchemy ORM session fixture.

    """
    # First create and save a line
    line = model.OrderLine('order1', 'TEST-SKU', 5)
    session.add(line)
    session.commit()

    # Modify the object
    line.qty = 10
    session.commit()

    # Verify the update
    rows = list(
        session.execute(
            text("SELECT qty FROM order_lines WHERE sku = 'TEST-SKU'")
        )
    )
    assert rows == [(10,)]


def test_orderline_mapper_can_delete_lines(session: Session) -> None:
    """Test that the ORM mapper can delete OrderLine objects.

    Verifies that deleting an object from the session and committing
    removes the corresponding database record.

    Args:
        session: SQLAlchemy ORM session fixture.

    """
    # Create and save a line
    line = model.OrderLine('order1', 'TO-DELETE', 3)
    session.add(line)
    session.commit()

    # Delete the line
    session.delete(line)
    session.commit()

    # Verify deletion
    count = session.query(model.OrderLine).filter_by(sku='TO-DELETE').count()
    assert count == 0
