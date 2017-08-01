# USAGE
# python facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg

# import the necessary packages
from imutils import face_utils
import argparse
import cv2
import dlib
import imutils

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

def emojify(detector, predictor, originalEmojiImg):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, image = video_capture.read()

        image = imutils.resize(image, width=500)
        draw_faces(image, detector, predictor, originalEmojiImg)

        cv2.imshow('Video', image)
        if cv2.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True,
        help="path to facial landmark predictor")
    args = vars(ap.parse_args())

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    # TODO: replace with a real path. maybe use a command line path?
    originalEmojiImg = cv2.imread("/Users/benlerner/Desktop/computer_vision/emoji/images/emoji/Neutral_Face_Emoji.png", -1)
    emojify(detector, predictor, originalEmojiImg)

if __name__ == "__main__":
    main()
