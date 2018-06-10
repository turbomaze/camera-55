import os
import cv2
import time
import numpy as np
import datetime
from mail import send_email

# webcam
cap = cv2.VideoCapture(1)

# config
memory_size = 5
stddev_cutoff = 2.5
last_email = 0
email_every_x = 30
email_username = os.environ['USERNAME']
email_password = os.environ['PASSWORD']
kernel = np.ones((5,5),np.float32)/25

# state
num_frames = 0
last_frames = []
last_magnitudes = []
for i in range(memory_size):
  last_frames.append(np.zeros((960, 1280)))
  last_magnitudes.append(0)
mean, variance = 0, 0

while True:
    # Capture frame-by-frame
    _, frame = cap.read()
    num_frames += 1

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    diff = gray - last_frames.pop(0)
    last_magnitudes.pop(0)
    last_frames.append(gray)
    magnitude = np.sum(np.absolute(diff))
    last_magnitudes.append(magnitude)
    window_mag = sum(last_magnitudes)
    variance = (variance * (num_frames - 1) + (window_mag - mean)**2) / num_frames
    mean = (mean * (num_frames - 1) + window_mag) / num_frames
    stddev = variance ** 0.5

    z_score = (window_mag - mean) / stddev
    anomaly = abs(z_score) > stddev_cutoff
    print round(abs(z_score), 2)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    if anomaly:
        cv2.imshow('frame', frame)
        filename = './data/frame-%d.jpg' % int(time.time() * 1000)
        cv2.imwrite(filename, frame)
        print 'Saved to %s' % filename
        if num_frames - last_email > email_every_x:
            last_email = num_frames
            now = datetime.datetime.now()
            walltime = '%d:%d' % (now.hour, now.minute)
            send_email(
                email_username, email_password,
                'pkt-camera-55@mit.edu',
                '[notice] MOTION DETECTED @ %s' % walltime,
                'Motion detected. See attached image.\n\nyitb,\nCamera 55 Bot',
                filename
            )
    else:
        cv2.imshow('frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
