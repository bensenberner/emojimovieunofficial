import cv2

video_capture = cv2.VideoCapture(0)

while True:
    # Capture video feed
    ret, frame = video_capture.read()

    # Create greyscale image from the video feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
