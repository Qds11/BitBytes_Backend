from flask import Blueprint
#  music_generation_prompt_bp is a blueprint instance named music_generation_prompt
music_generation_prompt_bp = Blueprint('music_generation_prompt', __name__)

# Import routes to register them with the blueprint
from . import routes
