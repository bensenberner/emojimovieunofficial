from operator import itemgetter
from emojify import draw_faces
import cv2
import imutils
import numpy as np

def process_img(detector, predictor, old_img, original_emoji_img):
    # TODO: confirm type of image
    img_arr = np.fromstring(old_img, np.uint8)
    img_decoded = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    shrunk_img = imutils.resize(img_decoded, width=600, height=400)
    emojified_img = draw_faces(shrunk_img, detector, predictor, original_emoji_img)
    # emojified_image = draw(raw_image)
    # We are using Motion JPEG, but OpenCV defaults to capture raw images,
    # so we must encode it into JPEG in order to correctly display the
    # video stream.

    # TODO: used to compress the picture and improve speed
    params = {
        "CV_IMWRITE_JPEG_QUALITY": 50
    }
    ret, jpeg = cv2.imencode('.jpg', emojified_img)
    return jpeg.tobytes()


class VideoCamera(object):
    def __init__(self, original_emoji_img, detector, predictor):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # TODO: change this for javascript
        # self.video = cv2.VideoCapture(0)
        # TODO: take out these hardcodings!
        self.original_emoji_img = original_emoji_img
        self.detector = detector
        self.predictor = predictor
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_live_frame(self):
        # TODO: clean this up a little
        try:
            success, raw_img = self.video.read()
        except AttributeError:
            return None
        # TODO: do not hardcode
        shrunk_img = imutils.resize(raw_img, width=600, height=400)
        emojified_img = draw_faces(shrunk_img, self.detector, self.predictor,
                self.original_emoji_img)
        # emojified_image = draw(raw_image)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        # TODO: used to compress the picture and improve speed
        params = {
            "CV_IMWRITE_JPEG_QUALITY": 50
        }
        ret, jpeg = cv2.imencode('.jpg', emojified_img)
        return jpeg.tobytes()

