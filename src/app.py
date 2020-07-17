from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS

from routes import urls


def index():
    return '<h1>API for FACE DETECTION </h1>'


# Create flask web application
app = Flask(__name__)

# cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config.from_object('config')  # load settings


app.add_url_rule('/', 'index', index)  # simple greeting in /

# Create access point for api rest
app_bp = Blueprint('api', __name__)
# Create api rest
api = Api(app_bp)

# Add urls for api rest
for url in urls:
    api.add_resource(url['resource'], url['path'], endpoint=url['endpoint'])

# Add access point to flask app
app.register_blueprint(app_bp, url_prefix='/api')
