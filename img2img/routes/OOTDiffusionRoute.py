from flask import Blueprint
OOTDiffusionRoutes = Blueprint('OOTDiffusionRoutes', __name__)

@OOTDiffusionRoutes.route('/test', methods=['GET'])
def test():
    return 'it works!'