from flask import request, jsonify
from schemas import order_schema, orders_schema
import services.orderServices as orderServices
from marshmallow import ValidationError
from application.caching import cache


def save():
    try:
        order_data = order_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400

    order_save = orderServices.save(order_data)
    if order_save is not None:
        return order_schema.jsonify(order_save), 201
    else:
        return jsonify({'message': 'Fallback method error activated', 'body': order_data}), 400

def find_all():
    orders = orderServices.find_all()
    return orders_schema.jsonify(orders), 200
