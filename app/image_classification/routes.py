from flask import request, jsonify
from . import image_classification_bp

@image_classification_bp.route('/', methods=['POST'])
def classify_image():
    # Add your image classification code here
    print("hello")
    return jsonify({'result': 'image classified'})
