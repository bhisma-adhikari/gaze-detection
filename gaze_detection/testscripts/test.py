import glob
import os

from gaze_detection.definitions import *
from gaze_detection.models import Face
from gaze_detection.utils import *
from gaze_detection.exceptions import *
import numpy as np

def main():
    paths = glob.glob(os.path.join(PATH_PKG, 'data/images/faces/*.*'))
    for p in paths:
        print('------------------------')
        try:
            face = Face.from_filepath(p)
        except NoFaceDetectedException:
            print('No face detected')
            continue
        except MultipleFacesDetectedException:
            print('Multiple faces detected')
            continue

        print('right :', face.right_eye.orientation)
        print('left  :', face.left_eye.orientation)

        face.gray = cv2.resize(face.gray, (500, 500))
        face.show()
        cv2.destroyAllWindows()


def test():
    try:
        face = Face.from_filepath('/home/ad718/Pictures/Webcam/2019-01-09-213244.jpg')
    except NoFaceDetectedException:
        print('No face detected')
    except MultipleFacesDetectedException:
        print('Multiple faces detected')

    print('right :', face.right_eye.orientation)
    print('left  :', face.left_eye.orientation)

    face.gray = cv2.resize(face.gray, (500, 500))
    face.show()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test()
    # main()