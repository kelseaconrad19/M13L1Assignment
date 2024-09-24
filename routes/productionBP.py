from flask import Blueprint
from controllers.productionController import save, find_all, production_efficiency
from services.productionServices import total_quantity_by_employee

production_blueprint = Blueprint('production_bp', __name__)
production_blueprint.route('/', methods=['POST'])(save)
production_blueprint.route('/', methods=['GET'])(total_quantity_by_employee)
production_blueprint.route('/production_efficiency', methods=['GET'])(production_efficiency)