from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    # Import Blueprints
    from .image_classification import image_classification_bp
    from .music_generation import music_generation_bp

    # Register Blueprints
    app.register_blueprint(image_classification_bp, url_prefix='/api/image_classification')
    app.register_blueprint(music_generation_bp, url_prefix='/api/music_generation')

    return app
