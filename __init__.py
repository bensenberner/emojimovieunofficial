#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for
from emojify import process_img
from datetime import datetime
from sys import platform
import os
import base64
import cognitive_face as CF
import cv2
import dlib

# TODO: consolidate strings
app = Flask(__name__, static_url_path='/static')
static_folder = 'static/'
# TODO: TAKE THIS OUT OF PROD
CF_KEY = os.environ["CF_KEY"]

@app.route('/')
def index():
    return redirect(url_for('emojify'))

@app.route('/emojify', methods = ['GET', 'POST'])
def emojify():
    if request.method == 'POST':
        screenshot_raw = request.form['screenshot']
        head, screenshot_b64 = screenshot_raw.split(',', 1)
        screenshot_decoded = base64.b64decode(screenshot_b64)
        # save screenshot for API call
        curr_time = str(int(datetime.timestamp(datetime.now())*1000000))
        filename = curr_time + '.jpg'
        full_file_path = static_folder + filename
        with open(full_file_path, 'wb') as f:
            f.write(screenshot_decoded)
        print(url_for("static", filename = filename))
        processed_screenshot = process_img(detector, predictor,
                screenshot_decoded, original_emoji_img)
        final_img = base64.b64encode(processed_screenshot)
        return final_img
    else:
        return render_template('index.html')

if __name__ == '__main__':
    # TODO: remove hardcodes, read from args instead
    original_emoji_path = "static/img/Neutral_Face_Emoji.png"
    original_emoji_img = cv2.imread(original_emoji_path, -1)
    dlib_pred_path = "shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(dlib_pred_path)
    detector = dlib.get_frontal_face_detector()
    port = 5000 if platform == 'darwin' else 80
    app.run(host='0.0.0.0', port=port)
