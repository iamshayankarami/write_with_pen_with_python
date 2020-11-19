import cv2
import numpy as np
import sys
import imutils, argparse
from collections import deque

video = cv2.VideoCapture(sys.argv[1])

low_blue = np.array([110,50,50])
high_blue = np.array([130,255,255])
while True:
    ret, frame = video.read()
    if frame is None:
        break
    #frame = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA)
    blure = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blure, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low_blue, high_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cuts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cuts = imutils.grab_contours(cuts)
    cetnter = None
    if len(cuts) > 0:
        c = max(cuts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print(center)
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0,255,0), -1)
    cv2.imshow("frame", frame)
    if cv2.waitKey(4) & 0XFF == ord("q"):
        break
cv2.destroyAllWindows()
