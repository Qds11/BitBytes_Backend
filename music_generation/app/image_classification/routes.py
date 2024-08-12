from flask import request, jsonify
from . import image_classification_bp  # Import the Blueprint from the same module
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import cv2
import os
import pickle
from ..limiter import limiter
from io import BytesIO

# Path to the models and binarizers directory
MODELS_DIR = '/app/assets/models/'
BINARIZERS_DIR = '/app/assets/binarizers/'
# MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
# BINARIZERS_DIR = os.path.join(os.path.dirname(__file__), 'binarizers')

IMAGE_DIMS = (60, 60, 3)

# Allowed image types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_FORMAT = 'JPEG'
RESIZE_DIMENSIONS = (800, 800)  # Example resize dimensions

# Load the pre-trained model
model_path = os.path.join(MODELS_DIR, 'multi_output_model.h5')
print(f"Loading model from: {model_path}")
model = tf.keras.models.load_model(model_path)

# Load the LabelBinarizers
with open(os.path.join(BINARIZERS_DIR, "articleTypeLB.pkl"), 'rb') as f:
    articleTypeLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, "genderLB.pkl"), 'rb') as f:
    genderLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, "baseColourLB.pkl"), 'rb') as f:
    baseColourLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, "seasonLB.pkl"), 'rb') as f:
    seasonLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, "usageLB.pkl"), 'rb') as f:
    usageLB = pickle.load(f)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_classification_bp.route('/', methods=['POST'])
@limiter.limit("10/minute")
def classify_image():
    print(f"File Retrieved: {request.files['img']}")
    if 'img' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['img']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            # Convert the image to an OpenCV format
            in_memory_file = BytesIO()
            file.save(in_memory_file)
            npimg = np.frombuffer(in_memory_file.getvalue(), np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            # Resize the image for the model
            resized_image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
            resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            resized_image = preprocess_input(resized_image)
            resized_image = np.expand_dims(resized_image, axis=0)

            # Perform prediction
            classification = model.predict(resized_image)
            results = decode_classification(classification)

            return jsonify(results)
        except Exception as e:
            print(e)
            return jsonify({"error": "File processing failed"}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

def decode_classification(classification):
    (categoryProba, genderProba, baseColourProba, seasonProba, usageProba) = classification
    # Get the indices of the highest probabilities
    categoryIdx = categoryProba[0].argmax()
    genderIdx = genderProba[0].argmax()
    baseColourIdx = baseColourProba[0].argmax()
    seasonIdx = seasonProba[0].argmax()
    usageIdx = usageProba[0].argmax()

    # Decode the predictions
    categoryLabel = articleTypeLB.classes_[categoryIdx]
    genderLabel = genderLB.classes_[genderIdx]
    baseColourLabel = baseColourLB.classes_[baseColourIdx]
    seasonLabel = seasonLB.classes_[seasonIdx]
    usageLabel = usageLB.classes_[usageIdx]

    return f"Category: {categoryLabel}, Gender: {genderLabel}, Colour: {baseColourLabel}, Season: {seasonLabel}, Usage: {usageLabel}"
