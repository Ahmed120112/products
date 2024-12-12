from . import db
from .product import Product

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='cart_items')
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Cart {self.product.name}, Quantity: {self.quantity}>"