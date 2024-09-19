from flask import current_app
from sqlalchemy import select
from sqlalchemy.orm import Session
from application.database import db
from models import Order, Product, Customer
from circuitbreaker import circuit

def fallback_function(order):
    return None
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(order_data):
    session = db.session
    product_ids = [product['id'] for product in order_data['products']]
    products = session.query(Product).filter(Product.id.in_(product_ids)).all()
    # products = session.execute(select(Product).where(Product.id.in_(product_ids))).scalars().all()

    customer_id = order_data['customer_id']
    # customer = session.execute(select(Customer).where(Customer.id == customer_id)).scalars().first()
    customer = session.query(Customer).get(customer_id)

    if len(products) != len(product_ids):
        raise ValueError('One or more products not found')
    if not customer:
        raise ValueError(f'Customer with ID {customer_id} not found')

    print("Products:", products[0].name)
    new_order = Order(date=order_data['date'], customer_id=order_data['customer_id'])
    new_order.products.extend(products)
    try:
        session.add(new_order)
        session.commit()
    except Exception as e:
        session.rollback()
        raise

    session.refresh(new_order)
    for product in new_order.products:
        session.refresh(product)
    # new_order = Order(date=order_data['date'], customer_id=order_data['customer_id'], products=products)
    # db.session.add(new_order)
    # print("New order ID (before commit):", new_order.id)
    # db.session.flush()
    # print("New order ID (after commit):", new_order.id)
    # db.session.commit()
    # session.refresh(new_order)
    # for product in new_order.products:
    #     session.refresh(product)

    return new_order

def find_all():
    query = select(Order)
    orders = db.engine.execute(query).scalars().all()
    return orders
