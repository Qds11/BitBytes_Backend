from flask import Blueprint

image_classification_bp = Blueprint('image_classification', __name__)

# Import routes to register them with the blueprint
from . import routes