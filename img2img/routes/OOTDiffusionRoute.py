from pathlib import Path
import sys, json, random

PROJECT_ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Blueprint, request
from services.OOTDiffusionService import generateImage, validateGenerateImageRequest
from services.S3Service import hello_s3
from utils.APIError import InvalidAPIUsage

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

OOTDiffusionRoutes = Blueprint('OOTDiffusionRoutes', __name__)

@OOTDiffusionRoutes.route('/test', methods=['GET'])
def test():
    file = request.files['file']
    url = hello_s3(file)
    return {"message": url}, 200

@OOTDiffusionRoutes.route('/generate', methods=['POST'])
def generate():
    params = json.loads(request.form.get('params'))
    file = request.files['file']
    validateGenerateImageRequest(file,params)
    
    modelType = params.get('modelType')
    category = int(params.get('category'))
    modelSelection = int(params.get('modelSelection'))
    imageScale = float(params.get('imageScale'))
    nSteps = int(params.get('nSteps'))
    nSamples = int(params.get('nSamples')) 
    seed = random.randint(0, 2**32 - 1)

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        try:
            generatedImagesURLs = generateImage(0,modelType, category, file, modelSelection, imageScale, nSteps, nSamples, seed)
        except AttributeError as e:
            print(e)
            raise InvalidAPIUsage("Something went wrong",500)
        # return send_file(modelMap[3], mimetype='image/png')
        return {"message": generatedImagesURLs},200