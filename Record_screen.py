import numpy as np
import cv2, pyautogui, sys, time, pyaudio, wave

user_screen_size = pyautogui.size()
screen_size = (int(sys.argv[1]), int(sys.argv[2]))

channels = 1
chunk = 1024
sample_rate = 44100
record_secounds = 5
#FORMAT = pyaudio.paInt16
#p = pyaudio.PyAudio()
#stream = p.open(format=FORMAT, channels=channels, rate=sample_rate, input=True, output=True, franes_per_buffer=chunk)

Output = []
while True:
    #Show = {}
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #voice = stream.read(chunk)
    #Show["video"] = frame
    #Show["audio"] = voice
    #Output.append(Show)
    if cv2.waitKey(10) == ord("q"):
        break
cv2.destroyAllWindows()
print("test")
