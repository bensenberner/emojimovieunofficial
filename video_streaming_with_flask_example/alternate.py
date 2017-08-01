# This is some code I made earlier which was predicated on the idea of using
# specific facial landmarks to anchor the emoji. Figured I'd keep it around
# just in case it proved useful

    #    dst = cv2.add(roi_bg, roi_fg)

        # show the face number
        # cv2.putText(image, "Face #{}".
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
