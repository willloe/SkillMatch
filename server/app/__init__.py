import os
from flask import Flask
from flask_cors import CORS
from .routes import api  # This should point to app/routes/api.py

def create_app():
    app = Flask(__name__)

    # ✅ Define UPLOAD_FOLDER path
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    # Enable CORS
    CORS(app)

    from .routes import api
    app.register_blueprint(api, url_prefix="/")

    return app