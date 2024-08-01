from flask import Flask, request, abort
from routes.OOTDiffusionRoute import OOTDiffusionRoutes

app = Flask(__name__)
app.register_blueprint(OOTDiffusionRoutes)

if __name__ == '__main__':
    app.run(debug=True)