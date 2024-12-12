from models import db, Product

def get_all_products():
    products = Product.query.all()
    return [
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

def add_product(data):
    product = Product(
        name=data.get('name'),
        price=data.get('price'),
        description=data.get('description'),
        image_url=data.get('image_url'),
        category_id=data.get('category_id')
    )
    db.session.add(product)
    db.session.commit()
    return {'message': 'Product added successfully'}

def update_product(product_id, data):
    product = Product.query.get(product_id)
    if not product:
        return {'error': 'Product not found'}
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.description = data.get('description', product.description)
    product.image_url = data.get('image_url', product.image_url)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return {'message': 'Product updated successfully'}

def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {'error': 'Product not found'}
    db.session.delete(product)
    db.session.commit()
    return {'message': 'Product deleted successfully'}