#!/usr/bin/env python
from flask import Flask, render_template, request
from emojify import process_img
import base64
import cv2
import dlib

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        screenshot_raw = request.form['screenshot']
        head, screenshot_b64 = screenshot_raw.split(',', 1)
        screenshot_decoded = base64.b64decode(screenshot_b64)
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
    app.run(host='localhost', debug=True)
