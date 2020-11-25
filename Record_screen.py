import numpy as np
import cv2, pyautogui, sys, time, pyaudio, wave
from mss import mss
from PIL import Image

user_screen_size = pyautogui.size()
screen_size = (int(sys.argv[1]), int(sys.argv[2]))

bound_box = {'top': 20, 'left': 0, 'width': screen_size[0], 'height': screen_size[1]}

sct = mss()
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

while True:
    Data = {}
    frame = sct.grab(bound_box)
    frame = np.array(frame)
    sound = stream.read(1024)
    Data["screen"] = frame
    Data["audio"] = sound
    print(Data)
    R = cv2.resize(frame, (int(screen_size[0]/2), int(screen_size[1]/2)))
    cv2.imshow("screen", R)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        stream.stop_stream()
        stream.close()
        break
