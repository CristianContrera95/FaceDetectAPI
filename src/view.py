import os

from PIL import Image
import numpy as np

from flask import request
from flask_restful import Resource

from config import FACES_FOLDER
from utils import (
    detect_faces,
    who_is,
    load_images,
)


class FaceDetectView(Resource):

    def __init__(self):
        super(FaceDetectView).__init__()

    def post(self):
        if 'image' in request.files.keys():
            file = request.files['image']
            if file:
                file.seek(0)
                img = np.array(Image.open(file))
                results = who_is(img)
                return {'names': results}, 200
        if 'image' in request.form.keys():
            pass
            # img_encoded = request.form['image']
            # img = np.frombuffer(img_encoded, dtype=np.float64)
            # results = who_is(img)
            # return {'names': results}, 200
        if 'image' in request.json.keys():
            pass
            # img_encoded = request.json['image']
            # img = np.frombuffer(img_encoded, dtype=np.float64)
            # results = who_is(img)
            # return {'names': results}, 200
        return {}, 400


class FaceRegisterView(Resource):

    def __init__(self):
        super(FaceRegisterView).__init__()

    def get(self):
        images = os.listdir(FACES_FOLDER)
        return {'images': images}, 200

    def post(self):
        file = request.files['image']
        if file:
            name = request.form['name']
            ext = file.filename.split('.')[-1]
            if name is not None:
                file.save(os.path.join(FACES_FOLDER, name+'.'+ext))
                load_images()
                return 200
        return 400
