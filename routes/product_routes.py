from flask import Blueprint, jsonify, request
from controllers.product_controller import get_all_products, add_product, update_product, delete_product

product_blueprint = Blueprint('product', __name__, url_prefix='/api/products')

@product_blueprint.route('', methods=['GET'])
def get_products():
    return jsonify(get_all_products())

@product_blueprint.route('', methods=['POST'])
def create_product():
    data = request.json
    return jsonify(add_product(data))

@product_blueprint.route('/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    data = request.json
    return jsonify(update_product(product_id, data))

@product_blueprint.route('/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    return jsonify(delete_product(product_id))