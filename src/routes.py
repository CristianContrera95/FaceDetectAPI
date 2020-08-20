from view import FaceDetectView, FaceRegisterView

# list with each access point in dict format
urls = [
    {
        'resource': FaceDetectView,
        'path': '/face_detect',
        'endpoint': 'face_detect',
    },
    {
        'resource': FaceRegisterView,
        'path': '/face_register/<string:name>',
        'endpoint': 'face_register',
    }
]