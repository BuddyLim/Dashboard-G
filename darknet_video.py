from ctypes import *
import math
import random
import os
import subprocess
import cv2
import numpy as np
import time
import darknet
# import simpleaudio as sa 
import csv

#TODO: check FFMPEG to download FFMPEG static library
#TODO: parse video & warning audio into output video
#TODO: check resolution settings for the system
#TODO: create a GUI to for users to input the video
#TODO: Baseline average size of car 
#TODO: Interpolate the resolution of 512x512 to 1080p & 720p

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for counter,detection in enumerate(detections):
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(counter) + " "+ str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
        # if detection[0].decode() == "car":
        #     print("Width: " + str(w) +"\n" + "Height: " + str(h))
        #     if w > 140 and h > 80:
        #         wave_obj = sa.WaveObject.from_wave_file("bleepsfxwav.wav")
        #         subprocess.call(cmd,shell=True)
        #         play_obj = wave_obj.play()
        #         play_obj.wait_done()
    return img


netMain = None
metaMain = None
altNames = None
#cmd = 'ffmpeg -i bleepsfxwav.wav -map 0:0 -map 0:1 -map 1:0 -map 2:0 -c:v copy -c:a copy output.avi'
cmd = 'ffmpeg -i input.mp4 -i music.mp3 -codec:v copy -codec:a aac -b:a 192k \
-strict experimental -filter_complex "amerge,pan=stereo:c0<c0+c2:c1<c1+c3" \
-shortest output.mp4'

def YOLO():
    
    global metaMain, netMain, altNames, detections
    configPath = "cfg\yolov3.cfg"
    weightPath = "../../../yolov3.weights"
    metaPath = "data\coco.data"
    # wave_obj = sa.WaveObject.from_wave_file("bleepsfxwav.wav")
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("C:Users\\user\\Pictures\\test.mp4")
    cap.set(3, cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(4, cv2.CAP_PROP_FRAME_WIDTH)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0,
        (darknet.network_width(netMain), darknet.network_height(netMain)))

    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    ###
    upper_left = (50, 50)
    bottom_right = (300, 300)
    ###
    while True:

        prev_time = time.time()
        ret, frame_read = cap.read()
    
        #If end of video, break loop. In some IDEs like Spyder, without this code, 
        #the window frame will still persist and requires the user to force close via task manager
        if(np.shape(frame_read) == ()): 
            print("Broke the loop")     
            break 
        
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                interpolation=cv2.INTER_LINEAR)
        #TODO: Pause video so that we can get better car data
        #Draws black borders on the sides so that YOLO only detects the mostly the middle section of the video
        frame_resized = cv2.rectangle(frame_resized,(0,0),(90,416),(0,0,0),-1)
        frame_resized = cv2.rectangle(frame_resized,(326,0),(416,416),(0,0,0),-1)
        
        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.7)
        image = cvDrawBoxes(detections, frame_resized)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #print(1/(time.time()-prev_time))
        cv2.imshow('Warning-Sys', image)
        out.write(image)

        #Break the loop when Q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
            print('Broke the loop')
    cap.release()
    out.release()

if __name__ == "__main__":
    YOLO()