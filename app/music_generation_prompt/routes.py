from flask import request, jsonify
from . import music_generation_prompt_bp
from ..limiter import limiter

@music_generation_prompt_bp.route('/', methods=['POST'])
@limiter.limit("5/minute")
def generate_prompt():
    # Add your image classification code here
    print("hello")
    return jsonify({'result': 'image classified'})
