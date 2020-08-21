import os
import cv2
import numpy as np
import face_recognition as fr

from config import (
    FACES_FOLDER,
    FACE_LOCATION_MODEL,
    FACE_ENCODING_MODEL,
    FACE_COMPARE_MINTOL,
    FACE_COMPARE_MAXTOL,
    FACE_DOWNSCALE_IMAGE
)


FACES_KNOWS_ENCODE = []
FACES_KNOWS_NAME = []


def load_images():
    """
    Load images in 'FACES_FOLDER' directory, and update 'FACES_KNOWS_ENCODE', 'FACES_KNOWS_NAME'
    global variables with the faces in these images
    """
    global FACES_KNOWS_ENCODE, FACES_KNOWS_NAME

    FACES_KNOWS_ENCODE = []
    FACES_KNOWS_NAME = []
    for file in os.listdir(FACES_FOLDER):
        fr_image = fr.load_image_file(os.path.join(FACES_FOLDER, file))
        for face in fr.face_encodings(fr_image, num_jitters=50, model=FACE_ENCODING_MODEL):

            FACES_KNOWS_ENCODE.append(face)
            FACES_KNOWS_NAME.append(file.split('.')[0])
            break

    FACES_KNOWS_ENCODE = np.array(FACES_KNOWS_ENCODE)
    FACES_KNOWS_NAME = np.array(FACES_KNOWS_NAME)


def preprocessing(img, gray=False, from_opencv=False):
    img = cv2.resize(img, (0, 0), fx=FACE_DOWNSCALE_IMAGE, fy=FACE_DOWNSCALE_IMAGE)
    # h = img.shape[0]
    # w = img.shape[1]
    # h_output_size = int(h * FACE_DOWNSCALE_IMAGE)
    # w_output_size = int(w * FACE_DOWNSCALE_IMAGE)
    #
    # h_bin_size = h // h_output_size
    # w_bin_size = w // w_output_size
    #
    # img = img.reshape((h_output_size, h_bin_size,
    #                    w_output_size, w_bin_size, 3)).max(3).max(1)
    if from_opencv:
        img = img[:, :, ::-1]  # bgr to rgb
    if gray:
        rgb_weights = [0.2989, 0.5870, 0.1140]
        img = np.dot(img[..., :3], rgb_weights)
    return img


def who_is(img):
    """
    Parse each face in the 'img' and compare them against the faces in 'FACES_KNOWS_ENCODE'
    :param img: The image that contains zero, one or more faces. Must be numpy array.
    :return: A list with names, one for each face found in img
    """
    face_names = []
    img = preprocessing(img)  # for faster face recognition processing

    # Search face in img

    for n in range(1, 5):
        face_locs = fr.face_locations(img, number_of_times_to_upsample=n, model=FACE_LOCATION_MODEL)
        if face_locs:
            break
    else:
        return face_names

    face_encodings = np.array(fr.face_encodings(img, known_face_locations=face_locs,
                                                num_jitters=10+(2**(n+1)),  # n from previous for loop
                                                model=FACE_ENCODING_MODEL))

    for face_encoded in face_encodings:
        for tol in np.arange(FACE_COMPARE_MINTOL, FACE_COMPARE_MAXTOL, 0.1):
            # Compare with to all faces knows
            face_distances = fr.face_distance(FACES_KNOWS_ENCODE, np.array([face_encoded]))

            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] <= tol:
                # Found the person
                face_names.append({'name': FACES_KNOWS_NAME[best_match_index],
                                   'confidence': 1-face_distances[best_match_index]})
                break
        else:
            # Didn't seems anybody
            face_names.append({'name': 'Desconocido',
                               'confidence': 1})

    return face_names


load_images()
