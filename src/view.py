import os
import numpy as np
import cv2

from PIL import Image
from flask import request, send_file
from flask_restful import Resource
from config import FACES_FOLDER
from utils import who_is, load_images


class FaceRegisterView(Resource):

    def __init__(self):
        super(FaceRegisterView).__init__()

    def get(self, name):
        for file in os.listdir(FACES_FOLDER):
            if file.startswith(name):
                return send_file(os.path.join(FACES_FOLDER, file), as_attachment=True)
                # img = np.array(Image.open())
                # ext = file.split('.')[-1]
                # _, img_encoded = cv2.imencode('.'+ext, img)
                # return {'image': img_encoded}, 200
        return {'msg': f'image with name "{name}" not found'}, 400

    def post(self, name):
        """
        This endpoint allow register new face
        :param name: Name of person on image
        :param image: file object or bytes numpy array encoded with opencv.imencode()
        :return: 200 if can register otherwise 400
        """
        if 'image' in request.files.keys():
            file = request.files.get('image', None)
            ext = file.filename.split('.')[-1]
            if file and name and (ext in ['jpg', 'jpeg', 'png']):
                try:
                    file.save(os.path.join(FACES_FOLDER, name + '.' + ext))
                except Exception as ex:
                    return {'error': 'can\'t save new image', 'except': str(ex)}, 400
            else:
                return {'error': 'No name received or file not is {jpg, jpeg, png}'}, 400
        elif request.data:
            try:
                # convert string of image data to uint8
                nparr = np.frombuffer(request.data, np.uint8)
                # decode image
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # name = request.json.get('name', None)
                if name:
                    cv2.imwrite(os.path.join(FACES_FOLDER, name + '.' + 'jpg'), img)
                else:
                    return {'error': 'No name received'}, 400
            except Exception as ex:
                return {'error': 'bad image received', 'except': str(ex)}, 400

        load_images()
        return {'msg': 'Ok'}, 200

    def delete(self, name):
        for file in os.listdir(FACES_FOLDER):
            if file.startswith(name):
                os.remove(os.path.join(FACES_FOLDER, file))
                return {'msg': 'Ok'}, 200
        return {'msg': 'image not found'}, 400


class FaceListView(Resource):
    def __init__(self):
        super(FaceListView).__init__()

    def get(self):
        images = os.listdir(FACES_FOLDER)
        return {'images': images}, 200


class FaceDetectView(Resource):

    def __init__(self):
        super(FaceDetectView).__init__()

    def post(self):
        img = None
        if 'image' in request.files.keys():
            file = request.files['image']
            if file:
                # set file point at the begin of file
                file.seek(0)
                # read file as numpy array
                img = np.array(Image.open(file))
        elif request.data:
            try:
                # convert string of image data to uint8
                nparr = np.frombuffer(request.data, np.uint8)
                # decode image
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as ex:
                return {'error': 'bad image received', 'except': str(ex)}, 400

        # performance detection
        if img is not None:
            results = who_is(img)
            return {'people': results}, 200
        return {'error': 'Can\'t get an image from request'}, 400
