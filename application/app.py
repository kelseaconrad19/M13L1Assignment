from flask import Flask, jsonify, app
from flask_sqlalchemy.session import Session

from schema import ma
from limiter import limiter
from database import db
from models import *
import datetime

from routes.customerBP import customer_blueprint
from routes.employeeBP import employee_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.productionBP import production_blueprint

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    app.debug = True

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)

    return app

def configure_rate_limit():
    limiter.limit("5 per day")(customer_blueprint)


def init_info_data():
    session = db.session

    try:
        products = [
            Product(name="Shirt", price=12.99),
            Product(name="Pants", price=35.99),
            Product(name="Socks", price=9.99)
        ]
        session.add_all(products)
        session.commit()

        customers = [
            Customer(name="John Doe", email="john@example.com", phone="1231231234"),
            Customer(name="Jane Smith", email="jane@example.com", phone="9876543210")
        ]
        session.add_all(customers)
        session.commit()

        orders = [
            Order(customer_id=customers[0].id, quantity=5),
            Order(customer_id=customers[1].id, quantity=3)
        ]
        session.add_all(orders)
        session.commit()

        session.execute(order_product.insert().values(order_id=orders[0].id, product_id=products[0].id, quantity=2))
        session.execute(order_product.insert().values(order_id=orders[0].id, product_id=products[1].id, quantity=3))

        session.execute(order_product.insert().values(order_id=orders[1].id, product_id=products[1].id, quantity=1))
        session.execute(order_product.insert().values(order_id=orders[1].id, product_id=products[2].id, quantity=2))
        session.commit()

        employees = [
            Employee(name="Alice Johnson", position="Manager", production_id=None),
            Employee(name="Bob Williams", position="Worker", production_id=None)
        ]
        session.add_all(employees)
        session.commit()

        productions = [
            Production(quantity=100, product_id=products[0].id, date_produced=datetime.date(2024, 9, 15)),
            Production(quantity=200, product_id=products[1].id, date_produced=datetime.date(2024, 9, 16)),
            Production(quantity=300, product_id=products[2].id, date_produced=datetime.date(2024, 9, 17))
        ]
        session.add_all(productions)
        session.commit()

        employees[0].production_id = productions[0].id
        employees[1].production_id = productions[1].id
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix="/customers")
    app.register_blueprint(employee_blueprint, url_prefix="/employees")
    app.register_blueprint(order_blueprint, url_prefix="/orders")
    app.register_blueprint(product_blueprint, url_prefix="/products")
    app.register_blueprint(production_blueprint, url_prefix="/production")


if __name__ == "__main__":
    app = create_app('DevelopmentConfig')
    blueprint_config(app)
    configure_rate_limit()

    with app.app_context():
        db.drop_all()
        db.create_all()
        init_info_data()

    app.run(debug=True)