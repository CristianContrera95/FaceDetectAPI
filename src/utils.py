import os
import cv2
import numpy as np

import face_recognition as fr
from keras.models import load_model

from config import FACES_FOLDER, EMOTIONS


FACES_KNOWS_ENCODE = []
FACES_KNOWS_NAME = []

HAAR_CASCADES = [
    'haarcascade_frontalface_default.xml',
    'haarcascade_profileface.xml',
    # 'haarcascade_frontalcatface_extended.xml',
    # 'haarcascade_frontalface_alt.xml',
    # 'haarcascade_frontalface_alt_tree.xml',
]

FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + HAAR_CASCADES[0])
FACE_PROFILE = cv2.CascadeClassifier(cv2.data.haarcascades + HAAR_CASCADES[1])


def load_images():
    global FACES_KNOWS_ENCODE, FACES_KNOWS_NAME

    FACES_KNOWS_ENCODE = []
    FACES_KNOWS_NAME = []
    for file in os.listdir(FACES_FOLDER):
        for face in fr.face_encodings(fr.load_image_file(os.path.join(FACES_FOLDER, file))):

            FACES_KNOWS_ENCODE.append(face)
            FACES_KNOWS_NAME.append(file.split('.')[0])
            break

    FACES_KNOWS_ENCODE = np.array(FACES_KNOWS_ENCODE)
    FACES_KNOWS_NAME = np.array(FACES_KNOWS_NAME)


def preprocessing(img, gray=False):
    img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)  # for faster face recognition processing
    # img = img[:, :, ::-1]  # bgr to rgb
    if gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def detect_faces(img):
    """
    Detectar caras en un frame
    """
    if img is None:
        return

    img = preprocessing(img, gray=True)

    faces_front = FACE_CASCADE.detectMultiScale(img, 1.1, 4)
    faces_profile = FACE_PROFILE.detectMultiScale(img, 1.1, 4)

    rectangles = []
    for (x, y, w, h) in faces_front:
        for (x_, y_, w_, h_) in faces_profile:
            # Evitar superposicion de rectangulos 10% cercanos
            if (abs(x - x_)/img.shape[1]/100) < 10 and (abs(y - y_)/img.shape[1]/100) < 10:
                continue
            rectangles.append((x_, y_, w_, h_))
        rectangles.append((x, y, w, h))

    result = []
    for (x, y, w, h) in rectangles:
        # faces_detected.append(img)  # [y:y+h, x:x+w,:]) # pasar solo la cara o toda la imagen?
        # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        result.append((img, (x, y, w, h)))

    return result


def who_is(img):
    """
    Analiza cada cara en la cola faces_detected y las compara contra las caras que ya vio, si es nueva la guarda
    """
    img = preprocessing(img)

    face_locs = fr.face_locations(img, number_of_times_to_upsample=5)
    face_encodings = np.array(fr.face_encodings(img, face_locs))

    face_names = []
    for face in face_encodings:
        matches = fr.compare_faces(FACES_KNOWS_ENCODE, face, tolerance=0.7)
        name = 'Desconocido'
        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        face_distances = fr.face_distance(FACES_KNOWS_ENCODE, face_encodings)
        best_match_index = np.argmin(face_distances)
        if (True not in matches) and (min(face_distances) < 0.5):
            name = FACES_KNOWS_NAME[best_match_index]
        elif matches[best_match_index]:
            name = FACES_KNOWS_NAME[best_match_index]

        face_names.append(name)

    face_names = list(set(face_names))
    return face_names


load_images()
