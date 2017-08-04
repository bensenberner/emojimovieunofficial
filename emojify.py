# TODO: originated from pyimagesearch and mustache.io
from imutils import face_utils
import argparse
import cv2
import dlib
import imutils
import numpy as np

def process_img(detector, predictor, old_img, original_emoji_img):
    # Typical case
    if type(old_img) == bytes:
        img_arr = np.fromstring(old_img, np.uint8)
        img_decoded = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    # just in case it's already an ndarray
    elif type(old_image) == np.ndarray:
        img_decoded = old_image
    # this shouldn't ever happen
    else:
        raise TypeError("Input image datatype not supported")
        return None
    shrunk_img = imutils.resize(img_decoded, width=600, height=400)
    emojified_img = draw_faces(shrunk_img, detector, predictor, original_emoji_img)

    # TODO: will use this to compress the picture and improve speed (maybe)
    params = {
        "CV_IMWRITE_JPEG_QUALITY": 50
    }
    # encoding ot jpeg to display properly
    ret, jpeg = cv2.imencode('.jpg', emojified_img)
    return jpeg.tobytes()

def draw_faces(image, detector, predictor, originalEmojiImg):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):

        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, face_w, face_h) = face_utils.rect_to_bb(rect)

        # a hack, sometimes when the face goes off the screen the program crashes with
        # error: (-215) (mtype == CV_8U || mtype == CV_8S) && _mask.sameSize(*psrc1) in function binary_op
        # mostly seems to stem from face_w or face_h being 0
        if x <= 0 or y <= 0 or face_w <= 0 or face_h <= 0:
            break

        # configure emoji img
        emojiImg = imutils.resize(originalEmojiImg, width=face_w, height=face_h)
        face_w, face_h, face_d = emojiImg.shape
        emojiMask = emojiImg[:, :, 3]
        emojiImg = emojiImg[:, :, 0:3]
        emojiMaskInv = cv2.bitwise_not(emojiMask)

        # the region of interest is the face
        roi_gray = gray[y:y+face_h, x:x+face_w]
        # TODO: hack (why?)
        roi_color = image[y:y+face_h, x:x+face_w]

        # TODO: this will be different if I choose not to use the face bounding box
        roi_bg = cv2.bitwise_and(roi_color, roi_color, mask = emojiMaskInv)
        roi_fg = cv2.bitwise_and(emojiImg, emojiImg, mask = emojiMask)
        dst = cv2.add(roi_bg, roi_fg)
        roi_color[:,:] = dst

    return image
