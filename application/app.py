from flask import Flask
from schema import ma
from limiter import limiter
from database import db
from models import *

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

    app.run(debug=True)