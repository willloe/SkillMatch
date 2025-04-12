from flask import Flask
from flask_cors import CORS
from .routes import api  # This should point to app/routes/api.py

def create_app():
    app = Flask(__name__)

    # Enable CORS for all origins and routes (needed for frontend ↔ backend)
    CORS(app)

    # Register API blueprint
    app.register_blueprint(api)

    return app