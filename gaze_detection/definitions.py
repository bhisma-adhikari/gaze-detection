import os

DEBUG = False

PATH_PKG = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(PATH_PKG, "model")
LANDMARK_DETECTOR = os.path.join(MODEL_PATH, "shape_predictor_68_face_landmarks.dat")

EYE_WIDTH = 240  # eye width
EYE_HEIGHT = 120  # eye height

PATH_UPLOADS = os.path.join(PATH_PKG, 'data/uploads')
SUPPORTED_EXTENSIONS = ['jpg', 'jpeg', 'png']

PROCESSING_IMAGE = False


