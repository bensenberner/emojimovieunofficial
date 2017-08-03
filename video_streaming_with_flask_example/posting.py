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
import base64
# from camera import VideoCamera

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        screenshot_raw = request.form['screenshot']
        head, screenshot_b64 = screenshot_raw.split(',', 1)
        with open('imageShouldSave.png', 'wb') as fh:
            fh.write(base64.b64decode(screenshot_b64))
            # fh.write(str(screenshot_raw.split(',')[1].decode('base64')))
        # screenshot = base64.b64decode(screenshot_raw)
        # print(screenshot)
        # with open("imageToSave.png", "wb") as fh:
            # fh.write(screenshot)

        return "received a post request!"
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
