import numpy as np
import cv2
from gaze_detection.eye import Eye as LEye
from gaze_detection.definitions import EYE_WIDTH, EYE_HEIGHT, DEBUG
import operator
from gaze_detection.exceptions import NoFaceDetectedException, MultipleFacesDetectedException
from gaze_detection.utils import print_json


class GrayImg:
    def __init__(self, nparray, name=None):
        assert len(nparray.shape) == 2
        self.name = name
        self.gray = np.copy(nparray)  # ensure a fresh numpy array is made for this image
        self.blackness = self._blackness()
        self.bgr = cv2.cvtColor(nparray, cv2.COLOR_GRAY2BGR)

    @classmethod
    def from_filepath(cls, filepath, name=None):
        cvimg = cv2.imread(filepath, 0)
        return GrayImg(cvimg, name)

    @property
    def height(self):
        return self.gray.shape[0]

    @property
    def width(self):
        return self.gray.shape[1]

    def show(self, name=None, waitkey=0):
        cv2.imshow(name or self.name or 'image', self.gray)
        cv2.waitKey(waitkey)

    def show(self, name=None, waitkey=0):
        cv2.imshow(name or self.name or 'image', self.gray)
        cv2.waitKey(waitkey)
        # cv2.destroyAllWindows()

    def crop(self, xmin, xmax, ymin, ymax, name=None):
        """Return new GrayImg object by cropping"""
        return GrayImg(nparray=self.gray[ymin:ymax, xmin:xmax], name=name)

    def _blackness(self):
        """Return blackness in range [0,1]"""
        max_white = self.height * self.width * 255
        white = self.gray.sum()
        if max_white:
            white_score = white / max_white
        else:
            return 0
        black_score = 1 - white_score
        return black_score


class Eye(GrayImg):
    def __init__(self, nparray, name='eye'):
        super().__init__(nparray, name)

        self.gray = cv2.resize(self.gray, (EYE_WIDTH, EYE_HEIGHT))
        self._orientation = None

    @property
    def orientation(self):
        """Return CENTER/LEFT/RIGHT/LEFT_DOWN/RIGHT_DOWN"""

        if self._orientation is None:
            # filter
            self.gray[self.gray > 50] = 255

            right = self.crop(0, int(EYE_WIDTH / 3), int(EYE_HEIGHT / 4), int(EYE_HEIGHT * 3 / 4), name='right')
            right_down = self.crop(0, int(EYE_WIDTH / 3), int(EYE_HEIGHT / 2), EYE_HEIGHT, name='right-down')
            left = self.crop(int(EYE_WIDTH * 2 / 3), EYE_WIDTH, int(EYE_HEIGHT / 4), int(EYE_HEIGHT * 3 / 4),
                             name='left')
            left_down = self.crop(int(EYE_WIDTH * 2 / 3), EYE_WIDTH, int(EYE_HEIGHT / 2), EYE_HEIGHT, name='left-down')
            center = self.crop(int(EYE_WIDTH / 3), int(EYE_WIDTH * 2 / 3), int(EYE_HEIGHT / 3), int(EYE_HEIGHT * 2 / 3),
                               name='center')

            scores = {'RIGHT': right.blackness * 1.3,
                      'RIGHT_DOWN': right_down.blackness * 1.5,
                      'LEFT': left.blackness * 1.3,
                      'LEFT_DOWN': left_down.blackness * 1.5,
                      'CENTER': center.blackness}

            if DEBUG: print_json(scores)

            self._orientation = max(scores.items(), key=operator.itemgetter(1))[0]
        return self._orientation


class Face(GrayImg):
    def __init__(self, nparray, name='face'):
        """Raises Exception if no face is detected"""
        super().__init__(nparray, name)

        result = LEye.get_eye_image_and_location(self.gray)

        if result == 'No face Detected':
            raise NoFaceDetectedException
        elif result == 'More than one face':
            raise MultipleFacesDetectedException

        self.right_eye = Eye(result['right_eye']['image'], name='right eye')
        self.left_eye = Eye(result['left_eye']['image'], name='left_eye')

    @classmethod
    def from_filepath(cls, filepath, name=None):
        cvimg = cv2.imread(filepath, 0)
        return Face(cvimg, name)


if __name__ == '__main__':
    nparray = cv2.imread('/home/ad718/Pictures/bhisma.jpg', 0)

    face_img = Face(nparray)
    print('right :', face_img.right_eye.orientation)
    print('left :', face_img.left_eye.orientation)
