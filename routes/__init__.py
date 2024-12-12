def init_routes(app):
    from .product_routes import product_blueprint
    from .cart_routes import cart_blueprint
    from .admin_routes import admin_blueprint
    from .home_routes import home_blueprint

    app.register_blueprint(product_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)