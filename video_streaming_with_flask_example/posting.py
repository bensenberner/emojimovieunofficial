#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, request
from camera import process_img
import base64
import cv2
import dlib
# from camera import VideoCamera

app = Flask(__name__)

# TODO: remove hardcodes
original_emoji_path = "/Users/benlerner/Desktop/computer_vision/emoji/images/emoji/Neutral_Face_Emoji.png"
original_emoji_img = cv2.imread(original_emoji_path, -1)
dlib_pred_path = "/Users/benlerner/Desktop/computer_vision/emoji/video_streaming_with_flask_example/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dlib_pred_path)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        screenshot_raw = request.form['screenshot']
        head, screenshot_b64 = screenshot_raw.split(',', 1)
        screenshot_decoded = base64.b64decode(screenshot_b64)
            # fh.write(str(screenshot_raw.split(',')[1].decode('base64')))
        # screenshot = base64.b64decode(screenshot_raw)
        # print(screenshot)
        # with open("imageToSave.png", "wb") as fh:
        # fh.write(screenshot)

        processed_screenshot = process_img(detector, predictor,
                screenshot_decoded, original_emoji_img)
        final_img = base64.b64encode(processed_screenshot)
        return final_img
    else:
        # return "received a GET request"
        return render_template('test.html')
    # return render_template('index.html')

# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera(original_emoji_img, detector, predictor)),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
