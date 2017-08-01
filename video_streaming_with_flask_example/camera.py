from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from operator import itemgetter
from emojify import draw_faces

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # TODO: take out these hardcodings!
        self.originalEmojiImg = cv2.imread("/Users/benlerner/Desktop/computer_vision/emoji/images/emoji/Neutral_Face_Emoji.png", -1)

        dlib_pred_path = "/Users/benlerner/Desktop/computer_vision/emoji/video_streaming_with_flask_example/shape_predictor_68_face_landmarks.dat"
        print("how often does this happen")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(dlib_pred_path)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, raw_img = self.video.read()
        # TODO: do not hardcode
        shrunk_img = imutils.resize(raw_img, width=600, height=400)
        emojified_img = draw_faces(shrunk_img, self.detector, self.predictor,
                self.originalEmojiImg)
        # emojified_image = draw(raw_image)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', emojified_img)
        return jpeg.tobytes()
