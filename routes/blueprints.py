from flask import Blueprint
from controllers.customerController import save, find_all

customer_blueprint = Blueprint('customer_bp', __name__)
customer_blueprint.post('/')(save)
customer_blueprint.get('/')(find_all)

employee_blueprint = Blueprint('employee', __name__)
employee_blueprint.post('/')(save)
employee_blueprint.get('/')(find_all)

order_blueprint = Blueprint('order', __name__)
order_blueprint.post('/')(save)
order_blueprint.get('/')(find_all)

product_blueprint = Blueprint('product', __name__)
product_blueprint.post('/')(save)
product_blueprint.get('/')(find_all)

production_blueprint = Blueprint('production', __name__)
production_blueprint.post('/')(save)
production_blueprint.get('/')(find_all)