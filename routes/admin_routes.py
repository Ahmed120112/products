from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/products')
def manage_products():
    return render_template('admin_products.html')