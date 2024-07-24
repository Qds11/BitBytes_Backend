from flask import request, jsonify
from . import music_generation_bp

@music_generation_bp.route('/', methods=['GET'])
def classify_image():
    # Add your image classification code here
    return jsonify({'result': 'music generated'})
