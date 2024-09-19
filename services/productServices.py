from sqlalchemy.orm import Session
from application.database import db
from models import Product
from circuitbreaker import circuit
from sqlalchemy import select

def fallback_function(product):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(product_data):
    if product_data["name"] == "Failure":
        raise Exception("Failure")
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(name=product_data["name"], price=product_data["price"])
            db.session.add(new_product)
            db.session.commit()
        db.session.refresh(new_product)
        return new_product

def find_all():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products