# USAGE
# python facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg

# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from operator import itemgetter

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
    help="path to facial landmark predictor")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# TODO: replace with a real path
originalEmojiImg = cv2.imread("/Users/benlerner/Desktop/computer_vision/emoji/images/emoji/Neutral_Face_Emoji.png", -1)

# load the input image, resize it, and convert it to grayscale
# image = cv2.imread(args["image"])
video_capture = cv2.VideoCapture(0)
while True:
    ret, image = video_capture.read()

    image = imutils.resize(image, width=500)
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
        if x <= 0 or y <= 0 or face_w <= 0 or face_h <= 0:
            break

        cv2.rectangle(image, (x, y), (x + face_w, y + face_h), (0, 255, 0), 2)

        # show the face number
        cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

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

    cv2.imshow('Video', image)
    if cv2.waitKey(1) == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()




    #    dst = cv2.add(roi_bg, roi_fg)

        # show the face number
        # cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # eyes
        # leftEye = np.mean(shape[36:42, :], axis=0)
        # rightEye = np.mean(shape[43:48, :], axis=0)

        # lip edges
        # leftLipIndices = itemgetter(48, 49, 59, 60)
        # rightLipIndices = itemgetter(53, 54, 55, 64)
        # leftLip = np.mean(leftLipIndices(shape), axis=0)
        # rightLip = np.mean(rightLipIndices(shape), axis=0)
        # keyFacePoints = np.float32([leftEye, rightEye, leftLip, rightLip])

        # middle of mouth
        # mouth = np.mean(shape[60:68, :], axis=0)
        # keyFacePoints = np.float32([leftEye, rightEye, mouth])

        # leftEmojiEye = (223, 262)
        # rightEmojiEye = (412, 262)
        # leftEmojiLip = (215, 414)
        # rightEmojiLip = (420, 414)
        # emojiMouth = (320, 414)

        # keyEmojiPoints = np.float32([leftEmojiEye, rightEmojiEye, leftEmojiLip, rightEmojiLip])
        # keyEmojiPoints = np.float32([leftEmojiEye, rightEmojiEye, emojiMouth])

        # perspective transformation
        # M = cv2.getPerspectiveTransform(keyEmojiPoints, keyFacePoints)
        # dst = cv2.warpPerspective(emojiImg, M, (640, 640))

        # affine transformation
        # M = cv2.getAffineTransform(keyEmojiPoints, keyFacePoints)
        # dst = cv2.warpAffine(emojiImg, M, (640, 640))
        # cv2.imshow("warped", dst)

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        # for float_x, float_y in keyFacePoints:
            # x = int(float_x)
            # y = int(float_y)
            # cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

        # for float_x, float_y in keyEmojiPoints:
            # x = int(float_x)
            # y = int(float_y)
            # cv2.circle(emojiImg, (x, y), 1, (0, 0, 255), -1)

    # show the output image with the face detections + facial landmarks
    # cv2.imshow('emoj', emojiImg)
# cv2.imshow("Output", image)
# cv2.waitKey(0)
