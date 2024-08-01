from flask import Blueprint

music_generation_bp = Blueprint('music_generation', __name__)

from . import routes
