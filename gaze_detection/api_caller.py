"""This module is to demonstrate how to invoke image-classifier api with python code
The face-image to be classified is assumed to be in image_file_path"""

import requests

image_file_path = '/home/ad718/projects/gaze-detection/gaze_detection/data/images/faces/face1.jpg'

response = requests.post(url='http://localhost:5000/api/gaze-detection/classify-image',
                         files={'face_image': open(image_file_path, 'rb')})

print(response.status_code)
print(response.text)
