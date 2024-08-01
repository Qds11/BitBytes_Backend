from flask import Flask
from .limiter import limiter
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object('app.config.Config')

    # Initialize limiter with app
    limiter.init_app(app)

    # Import Blueprints
    from .image_classification import image_classification_bp
    from .music_generation import music_generation_bp
    from .music_generation_prompt import music_generation_prompt_bp

    # Register Blueprints
    app.register_blueprint(image_classification_bp, url_prefix='/api/image_classification')
    app.register_blueprint(music_generation_bp, url_prefix='/api/music_generation')
    app.register_blueprint(music_generation_prompt_bp, url_prefix='/api/music_generation_prompt')

    return app
