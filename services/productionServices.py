from flask import jsonify
from sqlalchemy.orm import Session
from application.database import db
from models import Production, Employee, Product
from circuitbreaker import circuit
from sqlalchemy import select, func

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
    session = db.session
    query = session.query(
        Employee.name,
        func.sum(Production.quantity).label('total_quantity')).join(Production, Employee.production_id == Production.id).group_by(Employee.name)
    result = query.all()
    production_totals = [{"employee_name": row[0], "total_quantity": row[1]} for row in result]
    return production_totals

def total_quantity_by_employee():
    result = find_all()
    return jsonify(result)


def evaluate_production_efficiency(date):
    session = db.session

    subquery = session.query(Production).filter(Production.date_produced == date).subquery()

    query = session.query(
        Product.name,
        func.sum(Production.quantity).label('total_quantity_produced')).join(Production, Production.product_id == Product.id).filter(Production.date_produced == date).group_by(Product.name)

    result = session.execute(query).all()

    production_efficiency = [{"product_name": row[0], "total_quantity_produced": row[1]} for row in result]

    return production_efficiency