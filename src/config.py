import os


FACES_FOLDER = os.path.join(os.path.curdir, 'faces')
CUDA = False

FACE_LOCATION_MODEL = 'hog' if not CUDA else 'cnn'  # face detection model to use for face_recognition library
FACE_ENCODING_MODEL = 'large'  # large or small

FACE_COMPARE_MINTOL = 0.3
FACE_COMPARE_MAXTOL = 0.7
FACE_DOWNSCALE_IMAGE = 0.25  # .75, .5, .25 (less value, less image size)
