from models import db, Cart, Product

def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {'error': 'Product not found'}
    cart_item = Cart.query.filter_by(product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    return get_cart()

def get_cart():
    cart_items = Cart.query.all()
    return [
        {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity
        }
        for item in cart_items
    ]

def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(product_id=product_id).first()
    if not cart_item:
        return {'error': 'Item not found in cart'}
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)
    db.session.commit()
    return get_cart()

def clear_cart():
    Cart.query.delete()
    db.session.commit()
    return {'message': 'Cart cleared successfully'}