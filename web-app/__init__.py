
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register blueprints or routes
    from .app import register_routes
    register_routes(app)

    return app
