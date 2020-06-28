import sys
import cv2
import mss
import time
import json
import numpy
from PIL import Image
from pynput import keyboard
from pyKey import pressKey, releaseKey
numpy.set_printoptions(threshold=sys.maxsize)


def read_json_file(cfg_path="options.cfg"):
    try:
        with open(cfg_path,"r") as file:
            cfg = json.load(file)
        return cfg
    except:
        return False


def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    if k == triggerkey:
        start_capturing(white_pixels, wait_interval, wait_frames, opencv_wait_ms)


def start_capturing(white_pixels, wait_interval, wait_frames, opencv_wait_ms):
    frame_counter = 0

    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 200, "height": 50}
        while True:
            img = numpy.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # print(img[40][184], img[40][177], img[40][172], img[45][177], img[45][172], img[45][165])
            # print(img[40])

            for pixel in white_pixels:
                x, y = pixel[0], pixel[1]
                if(img[x][y] < 250):
                    frame_counter = 0
                    break
            else:
                frame_counter += 1
            

            if(frame_counter > wait_frames):
                print("trigger")
                time.sleep(wait_interval)
                print("keypress")
                pressKey(key="s")
                releaseKey(key="s")
                sys.exit()


            # print pixels
            for pixel in white_pixels:
                x, y = pixel[0], pixel[1]
                print(img[x][y], end="-")
            print("")


            # Display the picture
            if(opencv_wait_ms):
                cv2.imshow("OpenCV/Numpy normal", img)

                # Press "q" to quit
                cv2.waitKey(opencv_wait_ms)




# read cfg file
cfg = read_json_file()

if(not cfg):
    sys.exit()

wait_interval = cfg["wait_interval"]
wait_frames = cfg["wait_frames"]
triggerkey = cfg["triggerkey"]
white_pixels = cfg["white_pixels"]
opencv_wait_ms = cfg["opencv_wait_ms"]


# start listening
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()

