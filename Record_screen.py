import numpy as np
import cv2, pyautogui, sys, time, pyaudio, imutils, argparse
from collections import deque
from mss import mss
from PIL import Image
import mouse

screen_size = pyautogui.size()
#screen_size = (int(sys.argv[1]), int(sys.argv[2]))

bound_box = {'top': 20, 'left': 0, 'width': int(screen_size[0]/2), 'height': screen_size[1]-20}
print(bound_box)

cam = cv2.VideoCapture("/media/shayan/SHAYAN/SHAYAN 2/Shayan/TEST.mp4")
sct = mss()
#p = pyaudio.PyAudio()

#stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)
point = []
low_blue = np.array([110,50,50])
high_blue = np.array([130,255,255])
show_line = True
point = []
while True:
    Data = {}
    cam_ret, cam_frame = cam.read()
    frame = sct.grab(bound_box)
    frame = np.array(frame)
    Shape = frame.shape
    #mouse = pyautogui.position()
    #mouse_click = mouse.is_pressed("right")
    #print(mouse_click)
    cam_frame = cv2.resize(cam_frame, (Shape[1], Shape[0]), interpolation=cv2.INTER_AREA)
    blur = cv2.GaussianBlur(cam_frame, (11, 11), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low_blue, high_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    if cv2.waitKey(20) & 0xFF == ord("a"):
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
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if len(point) > 0:
            TR = point[len(point)-1]
            if TR[0] - center[0] >= 500:
                point=[]
        #center = (Shape[1]-Center[0], Center[1])
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 2)
        if show_line:
            point.append(center)
            for i in range(1, len(point)):
                if point[i-1] is None or point[i] is None:
                    continue
                cv2.line(frame, point[i-1], point[i], (255, 255, 0), 5)
            #mask2 = cv2.inRange(frame, (255, 255, 0), (255, 255, 0))
            #cv2.imshow("mask@", mask2)
    #sound = stream.read(1024)
    Data["screen"] = frame
    #Data["audio"] = sound
    #cv2.circle(frame, (int(mouse[0]), int(mouse[1]-15)), int(10), (0,0,255), 2)
    #R = cv2.resize(frame, (int(screen_size[0]/2), int(screen_size[1]/2)))
    R = cv2.resize(frame, (300, 300))
    cv2.imshow("screen", frame)
    cv2.imshow("camera", cam_frame)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        #stream.stop_stream()
        #stream.close()
        break
