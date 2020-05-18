import time

import cv2
from termcolor import colored
import json


def timeit(method):
    """
    A decorator used for time profiling functions and methods
    :param method:
    :return: time in ms for a method
    """

    def timed(*args, **kwargs):
        timeStart = time.time()
        result = method(*args, **kwargs)
        timeEnd = time.time()

        if 'log_time' in kwargs:
            name = kwargs.get('log_name', method.__name__.upper())
            kwargs['log_time'][name] = int((timeEnd - timeStart) * 1000)
        else:
            print('%r %2.2f ms' % (method.__name__, (timeEnd - timeStart) * 1000))
        return result

    return timed


def print_json(json_, title=None, color='blue'):
    """
    Print json data in a nicely formatted way

    :param json_: json data
    :type json_: dict
    :param title: title of the data (optional)
    :type title: str
    :return: None
    """
    if title:
        print(colored(text=title + ':', color='green'))

    print(colored(json.dumps(json_, indent=4, sort_keys=True), color=color))


def crop_img(img, xmin, xmax, ymin, ymax):

    return img[ymin:ymax, xmin:xmax]


def show_img(img, name=None):
    cv2.imshow(name, img)
    cv2.waitKey(0)


def blackness(img):
    """Return blackness in range [0,1]"""
    height, width = img.shape
    max_white = height * width * 255
    white = img.sum()
    if max_white:
        white_score = white / max_white
    else:
        return 0
    black_score = 1 - white_score
    return black_score
