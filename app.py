from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# إعداد قاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'e_commerce.db')}"
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# نموذج المنتجات
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}, ${self.price}>"

# نموذج السلة
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='cart_items')
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Cart {self.product.name}, Quantity: {self.quantity}>"

# API لإدارة المنتجات
@app.route('/api/products', methods=['POST'])
def add_product_api():
    try:
        data = request.json
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        image_url = data.get('image_url')
        category_id = data.get('category_id')

        if not name or not price or not category_id:
            return jsonify({'error': 'Name, price, and category_id are required!'}), 400

        new_product = Product(
            name=name,
            price=price,
            description=description,
            image_url=image_url,
            category_id=category_id
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Product added successfully!'}), 201
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred.'}), 500

@app.route('/api/products', methods=['GET'])
def get_products_api():
    try:
        products = Product.query.all()
        result = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'image_url': product.image_url,
                'category_id': product.category_id
            }
            for product in products
        ]
        return jsonify(result), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An internal error occurred.'}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product_api(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        data = request.json
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        product.image_url = data.get('image_url', product.image_url)
        product.category_id = data.get('category_id', product.category_id)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Product updated successfully!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred.'}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product_api(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred.'}), 500

# عرض صفحة المنتجات
@app.route('/')
def products():
    return render_template('products.html')

# عرض صفحة الإدارة
@app.route('/admin/products')
def admin_products():
    return render_template('admin_products.html')

# إدارة السلة
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.json.get('product_id')
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        cart_item = Cart.query.filter_by(product_id=product.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(product_id=product.id, quantity=1)
            db.session.add(cart_item)

        db.session.commit()
        return jsonify(get_cart_data()), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred.'}), 500

@app.route('/api/cart', methods=['GET'])
def get_cart():
    try:
        return jsonify(get_cart_data()), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch cart data.'}), 500

@app.route('/api/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    try:
        cart_item = Cart.query.filter_by(product_id=product_id).first()
        if not cart_item:
            return jsonify({'error': 'Item not found in cart'}), 404

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)

        db.session.commit()
        return jsonify(get_cart_data()), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred.'}), 500

@app.route('/api/cart', methods=['DELETE'])
def clear_cart():
    try:
        Cart.query.delete()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cart cleared successfully!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to clear cart. Please try again later.'}), 500

def get_cart_data():
    cart_items = Cart.query.all()
    return [
        {'id': item.product.id, 'name': item.product.name, 'price': item.product.price, 'quantity': item.quantity}
        for item in cart_items
    ]

if __name__ == '__main__':
    app.run(debug=True, port=8080)