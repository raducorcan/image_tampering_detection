"""
TRAIN WORKFLOW

1. RGB image => YCbCr image
2. YCbCr image => 32x32 (disjoint) patches
3. each patch => 270 features
4. array of 270 features fed into the network => authentic / tampered patch (based on patch info alone)
--- 5. use neighbourhood information to better predict label (not part of actual AI) ---
"""
import os
import random
import string

from flask import Flask, request, jsonify
from flask_cors import CORS

from feedforward.ff import Detector

app = Flask(__name__)
detector = Detector()
CORS(app)
app.config['UPLOAD_FOLDER'] = './res/temp'


def generate_filename():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))


@app.route("/detect", methods=['POST'])
def detect():
    f = request.files['image']
    filename = generate_filename() + ".png"
    f.save(f'./res/temp/{filename}')

    im, grayscale, percentage = detector.feedforward(f'./res/temp/{filename}')
    os.remove(f'./res/temp/{filename}')
    return jsonify({'im': im, 'grayscale': grayscale, 'percentage': percentage})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
