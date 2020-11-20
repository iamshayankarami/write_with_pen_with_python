import cv2
import numpy as np
import sys
import imutils, argparse
from collections import deque
import pyautogui as pgi

video = cv2.VideoCapture(0)

low_blue = np.array([110,50,50])
high_blue = np.array([130,255,255])
show_line = True
point = []
while True:
    ret, frame = video.read()
    Shape = frame.shape
    if frame is None:
        break
    #frame = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA)
    blure = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blure, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low_blue, high_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    if cv2.waitKey(4) & 0xFF == ord("w"):
        if show_line == True:
            show_line = False
            point = []
        else:
            show_line = True
    cuts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cuts = imutils.grab_contours(cuts)
    center = None
    if len(cuts) > 0:
        c = max(cuts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        Center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        center = (Shape[1]-Center[0], Center[1])
        #pgi.moveTo(center[0], center[1], duration=0)
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0,255,0), -1)
        if show_line:
            point.append(center)
            for i in range(1, len(point)):
                if point[i-1] is None or point[i] is None:
                    continue
                cv2.line(frame, point[i-1], point[i], (255,255,0), 2)
            mask2 = cv2.inRange(frame, (255,255,0), (255,255,0))
            cv2.imshow("mask@", mask2)
    #if center <= (100,100):
     #   point = []
    #print(center[1])
    cv2.imshow("frame", frame)
    if cv2.waitKey(4) & 0XFF == ord("a"):
        point = []
    if cv2.waitKey(4) & 0XFF == ord("q"):
        break
cv2.destroyAllWindows()
