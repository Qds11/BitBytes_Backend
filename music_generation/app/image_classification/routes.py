from flask import request, jsonify
from . import image_classification_bp  # Import the Blueprint from the same module
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import cv2
import os
import pickle
from ..limiter import limiter

# Path to the models and binarizers directory
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
BINARIZERS_DIR = os.path.join(os.path.dirname(__file__), 'binarizers')
TEST_IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')
IMAGE_DIMS = (60, 60, 3)

# Load the pre-trained model
model_path = os.path.join(MODELS_DIR, 'multi_output_model.h5')
model = tf.keras.models.load_model(model_path)

# Load the LabelBinarizers
with open(os.path.join(BINARIZERS_DIR, 'articleTypeLB.pkl'), 'rb') as f:
    articleTypeLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, 'genderLB.pkl'), 'rb') as f:
    genderLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, 'baseColourLB.pkl'), 'rb') as f:
    baseColourLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, 'seasonLB.pkl'), 'rb') as f:
    seasonLB = pickle.load(f)
with open(os.path.join(BINARIZERS_DIR, 'usageLB.pkl'), 'rb') as f:
    usageLB = pickle.load(f)

@image_classification_bp.route('/', methods=['POST'])
@limiter.limit("1/minute")
def classify_image():
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file part in the request"}), 400

    # file = request.files['file']

    # if file.filename == '':
    #     return jsonify({"error": "No selected file"}), 400

    file = os.path.join(TEST_IMG_DIR, 'blue-dress2.png')

    if file:
        # Read the image file
       # img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.imread(file)
        img = cv2.resize(img, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = preprocess_input(img)
        img = np.expand_dims(img, axis=0)

        # Perform prediction
        predictions = model.predict(img)
        # Assuming you have some function to decode predictions
        results = decode_predictions(predictions)  # Implement decode_predictions as needed

        return jsonify(results)

def decode_predictions(predictions):
    (categoryProba, genderProba, baseColourProba, seasonProba, usageProba) = predictions
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

    return {
        "Category": categoryLabel,
        "Gender": genderLabel,
        "Colour": baseColourLabel,
        "Season": seasonLabel,
        "Usage": usageLabel
    }
