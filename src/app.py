from flask import Flask, Blueprint
from flask_restful import Api
from routes import urls


def index():
    """Just I like do this"""
    return '<h1>API for FACE DETECTION </h1>'


app = Flask(__name__)  # Create flask web application

app.config.from_object('config')  # Load settings

app.add_url_rule('/', 'index', index)  # Simple greeting in /

app_bp = Blueprint('api', __name__)  # Create access point for api rest

api = Api(app_bp)  # Create api rest

# Add urls for api rest
for url in urls:
    api.add_resource(url['resource'], url['path'], endpoint=url['endpoint'])

# Add access point to flask app
app.register_blueprint(app_bp, url_prefix='/api')
