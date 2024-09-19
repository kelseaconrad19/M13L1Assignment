import flask
from schemas import product_schema, products_schema
import services.productServices as productService
from marshmallow import ValidationError
from application.caching import cache


def save():
    try:
        product_data = product_schema.load(flask.request.json)

    except ValidationError as err:
        return flask.jsonify(err.messages), 400

    product_save = productService.save(product_data)
    if product_save is not None:
        return product_schema.jsonify(product_save), 201
    else:
        return flask.jsonify({'message': 'Fallback method error activated', 'body': product_data}), 400

def find_all():
    products = productService.find_all()
    return products_schema.jsonify(products), 200