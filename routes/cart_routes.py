from flask import Blueprint, jsonify, request
from controllers.cart_controller import add_to_cart, get_cart, remove_from_cart, clear_cart, update_cart_item

cart_blueprint = Blueprint('cart', __name__, url_prefix='/api/cart')

# جلب محتوى السلة
@cart_blueprint.route('', methods=['GET'])
def fetch_cart():
    return jsonify(get_cart())

# إضافة منتج إلى السلة
@cart_blueprint.route('', methods=['POST'])
def add_item_to_cart():
    product_id = request.json.get('product_id')
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400
    return jsonify(add_to_cart(product_id))

# حذف منتج معين من السلة
@cart_blueprint.route('/<int:product_id>', methods=['DELETE'])
def remove_item_from_cart(product_id):
    return jsonify(remove_from_cart(product_id))

# تنظيف السلة بالكامل
@cart_blueprint.route('/clear', methods=['DELETE'])
def clear_items_from_cart():
    return jsonify(clear_cart())

# تحديث كمية منتج في السلة (زيادة/نقصان)
@cart_blueprint.route('/<int:product_id>', methods=['PUT'])
def update_item_quantity(product_id):
    data = request.json
    change = data.get('change')

    if change not in [1, -1]:
        return jsonify({"error": "Invalid change value. Must be 1 or -1"}), 400

    return jsonify(update_cart_item(product_id, change))