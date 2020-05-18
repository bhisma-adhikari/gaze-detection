# USAGE
# python eye.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg

import time

import cv2
import dlib
# import the necessary packages
from imutils import face_utils

from gaze_detection.definitions import LANDMARK_DETECTOR, DEBUG
from gaze_detection.utils import timeit

face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(LANDMARK_DETECTOR)
import numpy as np
from gaze_detection.definitions import EYE_HEIGHT, EYE_WIDTH


class Eye:

    @staticmethod
    def _crop_eye(image, eye_coord):
        """
        Gives rectangular crop
        :param face:
        :param eye_coord:
        :return:
        """
        x = eye_coord[0][0]
        y = eye_coord[1][1]
        w = eye_coord[3][0] - x
        h = eye_coord[4][1] - y

        cropped_image = image[y:y + h, x:x + w]

        return cv2.resize(cropped_image, (EYE_WIDTH, EYE_HEIGHT))

    @staticmethod
    def _get_cropped_eye(image, eye_cord):
        """
        Gives polygonal crop using cordinate from face landmark
        :param image:
        :param eye_cord:
        :return:
        """
        hull = cv2.convexHull(eye_cord)
        # --- Black image to be used to draw individual convex hull ---
        black = np.zeros_like(image)

        # black.fill(255)
        # img2 = image.copy()
        # black2 = black.copy()

        # --- Here is where I am filling the contour after finding the convex hull ---
        cv2.drawContours(black, [hull], -1, (255, 255, 255), -1)
        g2 = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)
        masked = cv2.bitwise_and(image, image, mask=g2)
        masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        g2 = cv2.bitwise_not(g2)
        img = masked + g2
        return img

    @classmethod
    def get_eye_image_and_location(cls, image):
        """
        Return cropped eye image and its coordinates
        :param image: np array, should be grayscale image
        :return:
        """
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        start = time.time()

        faces = face_detector(image)
        # print(time.time() - start)

        if not faces:
            return "No face Detected"
        if len(faces) > 1:
            return "More than one face"

        face_rect = faces[0]
        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        # (x, y, w, h) = face_utils.rect_to_bb(face_rect)
        # face_image = image[y:y + h, x:x + w]

        start = time.time()

        facial_landmarks = landmark_predictor(image, face_rect)

        # (x, y)-coordinates for the 68 facial landmarks
        # Check facial_landmarks_68markup-768x619.jpg to get the details for all the landmarks

        facial_landmarks = face_utils.shape_to_np(facial_landmarks)

        # print(time.time() - start)

        # Geting coordinate for the eyes
        right_eye_coord = facial_landmarks[36:42]
        left_eye_coord = facial_landmarks[42:48]

        start = time.time()

        left_eye_image = cls._get_cropped_eye(image, left_eye_coord)
        left_eye_image = cls._crop_eye(left_eye_image, left_eye_coord)
        right_eye_image = cls._get_cropped_eye(image, right_eye_coord)
        right_eye_image = cls._crop_eye(right_eye_image, right_eye_coord)

        # print(time.time() - start)

        if DEBUG:
            cv2.imshow("left", left_eye_image)
            cv2.imshow("right", right_eye_image)
            cv2.waitKey(0)

        return {
            "left_eye": {"image": left_eye_image, "cord": left_eye_coord},
            "right_eye": {"image": right_eye_image, "cord": right_eye_coord}
        }


if __name__ == "__main__":
    DEBUG = True


    @timeit
    def aaa():
        HEIGHT = 100
        WIDTH = 200
        path = "./data/images/faces/eye-patch.jpg"
        img = cv2.imread(path, 0)
        # img = cv2.resize(img, (WIDTH, HEIGHT))
        Eye.get_eye_image_and_location(img)


    print(aaa())
