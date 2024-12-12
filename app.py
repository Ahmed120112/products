from flask import Flask
from config import Config
from models import db
from routes import init_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)