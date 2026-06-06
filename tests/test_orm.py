"""Test the ORM."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from percival_cargo.domain import model


def test_orderline_mapper_can_load_lines(session: Session) -> None:
    """Test that OrderLine mapper can load lines from database."""
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
    """Test that OrderLine mapper can save lines to database."""
    new_line = model.OrderLine('order1', 'DECORATIVE-WIDGET', 12)
    session.add(new_line)
    session.commit()

    rows = list(
        session.execute(text('SELECT order_id, sku, qty FROM order_lines'))
    )
    assert rows == [('order1', 'DECORATIVE-WIDGET', 12)]
