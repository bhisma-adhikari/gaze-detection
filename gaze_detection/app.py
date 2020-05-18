import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import gaze_detection.definitions as defns
from gaze_detection.definitions import PATH_UPLOADS, SUPPORTED_EXTENSIONS
from gaze_detection.models import Face
from gaze_detection.exceptions import NoFaceDetectedException, MultipleFacesDetectedException
from gaze_detection.initializer import Initializer

app = Flask(__name__)
CORS(app)

@app.route('/api/gaze-detection/test')
def indextest():
    return render_template('index.html')

@app.route('/api/gaze-detection/reset')
def reset():
    defns.PROCESSING_IMAGE = False
    return jsonify({'msg': 'server reset'})


@app.route('/api/gaze-detection/classify-image', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({'message': 'Please, make a POST request instead'})
    if request.method == 'POST':
        if defns.PROCESSING_IMAGE:
            return jsonify({'ERROR': "Image processing in progress. Please, try again later"}), 503

        defns.PROCESSING_IMAGE = True
        try:
            file = request.files['face_image']
            print(type(file))
        except:
            return jsonify({'ERROR': "image file 'face_image' missing"}), 400
        finally:
            defns.PROCESSING_IMAGE = False

        ext = os.path.splitext(file.filename)[-1][1:].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            defns.PROCESSING_IMAGE = False
            return "invalid extension '{}'. Only {} supported".format(ext, SUPPORTED_EXTENSIONS), 400

        path = os.path.join(PATH_UPLOADS, '{}.{}'.format('face_img', ext))
        file.save(path)

        try:
            face = Face.from_filepath(path)
        except NoFaceDetectedException:
            return jsonify({'ERROR': 'No face detected in given image'}), 400
        except MultipleFacesDetectedException:
            return jsonify({'ERROR': 'Multiple faces detected in given image'}), 400

        except:
            return jsonify({'ERROR': 'Internal Server Error'}), 500
        finally:
            defns.PROCESSING_IMAGE = False

        return jsonify({'right_eye': face.right_eye.orientation,
                        'left_eye': face.left_eye.orientation})


@app.route('/api/gaze-detection/upload-image-file')
def image_upload_form():
    return render_template('upload-image.html')


@app.route('/api/gaze-detection/upload-image-file-local')
def image_upload_form_local():
    return render_template('upload-image-local.html')


if __name__ == '__main__':
    Initializer.initialize_folders()  # create upload directory, if needed
    app.run(port=10000, debug=True, host='0.0.0.0')
