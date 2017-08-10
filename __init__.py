from emojify import process_img
from flask import Flask, render_template, request, redirect, url_for, current_app
from sys import platform
import base64
import cognitive_face as CF
import cv2
import os

# TODO: consolidate strings
app = Flask(__name__, static_url_path='/static')
app_path = "./" if platform == 'darwin' else "/var/www/emojimovieunofficial/emojimovieunofficial/"

CF_KEY = os.environ["CF_KEY"]
CF.Key.set(CF_KEY)

@app.before_first_request
def load_emoji_imgs():
    # TODO: disgust and don't hardcode these (that's disgusting in itself)
    emotions = ["anger", "fear", "low_happy", "neutral", "surprise", "contempt", "high_happy", "med_happy", "sadness"]
    emoji_imgs = {}
    for emotion in emotions:
        path = app_path + "static/img/" + emotion + ".png"
        emoji_img = cv2.imread(path, -1)
        emoji_imgs[emotion] = emoji_img
    current_app.emoji_imgs = emoji_imgs

class pseudofile(object):
    def __init__(self, data):
        self.data = data
    def read(self):
        return self.data

@app.route('/')
def index():
    return redirect(url_for('emojify'))

@app.route('/emojify', methods = ['GET', 'POST'])
def emojify():
    if request.method == 'POST':
        screenshot_raw = request.form['screenshot']
        head, screenshot_b64 = screenshot_raw.split(',', 1)
        screenshot_decoded = base64.b64decode(screenshot_b64)
        image_obj = pseudofile(screenshot_decoded)
        # TODO: try catch in case the call fails
        analysis = CF.face.detect(image_obj, attributes='smile,emotion')
        processed_screenshot = process_img(screenshot_decoded, current_app.emoji_imgs, analysis)
        final_img = base64.b64encode(processed_screenshot)
        return final_img
    else:
        return render_template('index.html')

if __name__ == '__main__':
    port = 5000 if platform == 'darwin' else 5001
    app.run(host='0.0.0.0', port=port)
