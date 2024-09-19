from sqlalchemy.orm import Session
from application.database import db
from models import Production
from circuitbreaker import circuit
from sqlalchemy import select

def fallback_function(production):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(production_data):
    with Session(db.engine) as session:
        with session.begin():
            new_production = Production(product_id=production_data['product_id'], quantity=production_data['quantity_produced'], date_produced=production_data['date_produced'])
            db.session.add(new_production)
            db.session.commit()
        session.close()
        return new_production

def find_all():
    query = select(Production)
    production = db.engine.execute(query).scalars().all()
    return production