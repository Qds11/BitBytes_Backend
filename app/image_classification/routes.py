from flask import request, jsonify
from . import image_classification_bp
from ..limiter import limiter

@image_classification_bp.route('/', methods=['POST'])
@limiter.limit("1/minute")
def classify_image():
    # Add your image classification code here
    print("hello")
    return jsonify({'result': 'image classified'})
