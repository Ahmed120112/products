from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# تحديد المسار لقاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'e_commerce.db')}"
app.config['SECRET_KEY'] = 'your_secret_key'

# تهيئة SQLAlchemy و Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# تعريف النماذج
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='cart_items')
    quantity = db.Column(db.Integer, default=1)

# إضافة منتج إلى السلة
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
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

# زيادة الكمية لمنتج معين
@app.route('/increase_quantity', methods=['POST'])
def increase_quantity():
    product_id = request.json.get('product_id')
    cart_item = Cart.query.filter_by(product_id=product_id).first()

    if not cart_item:
        return jsonify({'error': 'Item not found in cart'}), 404

    cart_item.quantity += 1
    db.session.commit()
    return jsonify(get_cart_data()), 200

# تقليل الكمية لمنتج معين
@app.route('/decrease_quantity', methods=['POST'])
def decrease_quantity():
    product_id = request.json.get('product_id')
    cart_item = Cart.query.filter_by(product_id=product_id).first()

    if not cart_item:
        return jsonify({'error': 'Item not found in cart'}), 404

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)

    db.session.commit()
    return jsonify(get_cart_data()), 200

# مسح جميع المنتجات من السلة
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    Cart.query.delete()
    db.session.commit()
    return jsonify({'success': True}), 200

# الحصول على بيانات السلة
def get_cart_data():
    cart_items = Cart.query.all()
    return [
        {'id': item.product.id, 'name': item.product.name, 'price': item.product.price, 'quantity': item.quantity}
        for item in cart_items
    ]

# عرض المنتجات
@app.route('/')
def products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('products.html', products=products, categories=categories)

# عرض المنتجات حسب الفئة
@app.route('/category/<int:category_id>')
def products_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category.id).all()
    categories = Category.query.all()
    return render_template('products.html', products=products, categories=categories, selected_category=category.name)

# إدارة المنتجات - صفحة الإدارة
@app.route('/admin/products')
def admin_products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin_products.html', products=products, categories=categories)

# إضافة منتج جديد
@app.route('/admin/products/add', methods=['POST'])
def add_product():
    try:
        name = request.form.get('name')
        price = float(request.form.get('price', 0))
        description = request.form.get('description', '')
        image_url = request.form.get('image_url', '')
        category_id = request.form.get('category_id')

        if not name or price <= 0 or not category_id:
            return jsonify({'error': 'Name, valid price, and category are required!'}), 400

        new_product = Product(name=name, price=price, description=description, image_url=image_url, category_id=category_id)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Product added successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500

# تعديل منتج
@app.route('/admin/products/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        product.name = request.form.get('name', product.name)
        product.price = float(request.form.get('price', product.price))
        product.description = request.form.get('description', product.description)
        product.image_url = request.form.get('image_url', product.image_url)
        product.category_id = request.form.get('category_id', product.category_id)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Product updated successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500

# حذف منتج
@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True, port=8080)