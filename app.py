import cv2
import numpy as np

cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

num_frames = 0
last_frame = np.zeros((960, 1280))
mean = 0
variance = 0

while True:
    # Capture frame-by-frame
    _, frame = cap.read()
    num_frames += 1

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = gray - last_frame
    last_frame = gray
    magnitude = np.sum(np.absolute(diff))
    variance = (variance * (num_frames - 1) + (magnitude - mean)**2) / num_frames
    mean = (mean * (num_frames - 1) + magnitude) / num_frames
    stddev = variance ** 0.5

    if abs(magnitude - mean) > 2 * stddev:
        print 'ANOMALY!!'

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
