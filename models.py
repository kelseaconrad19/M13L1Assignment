from application.database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from typing import List

order_product = db.Table(
    'Order_Product',
    Base.metadata,
    db.Column('order_id', db.ForeignKey('Orders.id')),
    db.Column('product_id', db.ForeignKey('Products.id'))
)

class Customer(Base):
    __tablename__ = "Customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320))
    phone: Mapped[str] = mapped_column(db.String(15))
    orders: Mapped[list["Order"]] = db.relationship(back_populates='customer')

class Employee(Base):
    __tablename__ = 'Employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    position: Mapped[str] = mapped_column(db.String(320))

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    customer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Customers.id'))
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
    products: Mapped[List["Product"]] = db.relationship(secondary=order_product)

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

class Production(Base):
    __tablename__ = 'Production'
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Products.id'))
    date_produced: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)