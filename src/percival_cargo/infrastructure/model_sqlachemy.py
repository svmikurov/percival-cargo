"""SqlAlchemy ORM."""

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = MetaData()


class Order(Base):  # type: ignore
    """Order ORM."""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    lines = relationship('OrderLine', back_populates='order')


class OrderLine(Base):  # type: ignore
    """Order line ORM."""

    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    sku = Column(String(255))
    qty = Column(Integer)

    order = relationship(Order)
