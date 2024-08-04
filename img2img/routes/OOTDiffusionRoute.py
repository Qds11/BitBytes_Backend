from pathlib import Path
import sys, json, random

PROJECT_ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Blueprint, request, jsonify, send_from_directory,send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from services.OOTDiffusionService import generateImage

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

OOTDiffusionRoutes = Blueprint('OOTDiffusionRoutes', __name__)

@OOTDiffusionRoutes.route('/test', methods=['GET'])
def test():
    return 'it works!'

@OOTDiffusionRoutes.route('/generate', methods=['POST'])
def generate():
    params = json.loads(request.form.get('params'))
    file = request.files['file']
    
    if file == None:
        return {
            "message": "Bad request. No file found"
        }, 400
    if params == None:
        return {
            "message": "Bad request. No params found"
        }, 400
    
    if file.filename == '':
        return {
            "message": "Bad filename"
        }, 400
    
    modelType = params.get('modelType')
    category = params.get('category')
    modelSelection = int(params.get('modelSelection'))
    imageScale = float(params.get('imageScale'))
    nSteps = int(params.get('nSteps'))
    nSamples = int(params.get('nSamples')) 
    seed = random.randint(0, 2**32 - 1)

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        # TODO: Can't seem to send back a list of files. Maybe use S3 and send back a list of urls?
        generateImage(1,modelType, category, file, modelSelection, imageScale, nSteps, nSamples, seed)
        # return send_file(modelMap[3], mimetype='image/png')
        return {"message": "Success"},200