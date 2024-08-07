from flask import Flask, jsonify

from routes.OOTDiffusionRoute import OOTDiffusionRoutes
from utils.APIError import InvalidAPIUsage

app = Flask(__name__)
app.register_blueprint(OOTDiffusionRoutes)

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

if __name__ == '__main__':
    app.run(debug=True)