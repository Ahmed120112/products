from flask import Blueprint, jsonify, request
from controllers.cart_controller import add_to_cart, get_cart, remove_from_cart, clear_cart

cart_blueprint = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_blueprint.route('', methods=['GET'])
def fetch_cart():
    return jsonify(get_cart())

@cart_blueprint.route('', methods=['POST'])
def add_item_to_cart():
    product_id = request.json.get('product_id')
    return jsonify(add_to_cart(product_id))

@cart_blueprint.route('/<int:product_id>', methods=['DELETE'])
def remove_item_from_cart(product_id):
    return jsonify(remove_from_cart(product_id))

@cart_blueprint.route('', methods=['DELETE'])
def clear_items_from_cart():
    return jsonify(clear_cart())