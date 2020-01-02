from ctypes import *
import math
import random
import os
import subprocess
import cv2
import numpy as np
import time
import darknet
import pandas as pd
import simpleaudio as sa
import objecttrack
#import csv

#from pyimagesearch.centroidtracker import CentroidTracker


framecount = 0


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for counter, detection in enumerate(detections):
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
                    " [" + str(counter) + " " +
                    str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)

    del detections[:]
    return img


netMain = None
metaMain = None
altNames = None
listodetect = []
framecountlist = []
drawdetections = []

prev_h = 0
prev_w = 0

#cmd = 'ffmpeg -i bleepsfxwav.wav -map 0:0 -map 0:1 -map 1:0 -map 2:0 -c:v copy -c:a copy output.avi'
# cmd = 'ffmpeg -i input.mp4 -i music.mp3 -codec:v copy -codec:a aac -b:a 192k \
# -strict experimental -filter_complex "amerge,pan=stereo:c0<c0+c2:c1<c1+c3" \
# -shortest output.mp4'


def YOLO():

    global metaMain, netMain, altNames, framecount, listodetect, drawdetections, prev_h, prev_w

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

    cap = cv2.VideoCapture(
        "C:\\Users\\user\\Documents\\FYP\\RearEndAccident2(E)-1080.mp4")
    cap.set(3, cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(4, cv2.CAP_PROP_FRAME_WIDTH)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0,
        (darknet.network_width(netMain), darknet.network_height(netMain)))

    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                       darknet.network_height(netMain), 3)

    ot = objecttrack.objecttrack()

    while True:
        prev_time = time.time()
        ret, frame_read = cap.read()
        framecount = framecount + 1

        # If end of video, break loop. In some IDEs like Spyder, without this code,
        # the window frame will still persist and requires the user to force close via task manager
        if(np.shape(frame_read) == ()):
            print("Broke the loop\n")
            print("Framecount: " + str(framecount))
            break

        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
        detections = darknet.detect_image(
            netMain, metaMain, darknet_image, thresh=0.7)

        for detection in detections:
            # Own object tracking
            # 1. Get the bounding boxes and get the centroid
            # 2. Calculate the Eculidian distance between the previous centroid and current centroid
            # 3. Closest distance of previous centroid and current centroid is considered the same object
            # 4. Store the centroid and the bounding boxes in a list
            x, y, w, h = detection[2][0],\
                detection[2][1],\
                detection[2][2],\
                detection[2][3]
            if(90 < x < 326 and 90 < y < 326):
                if(w > 26 and h > 43):
                    ot.increasecounter()
                    # xmin, ymin, xmax, ymax = convertBack(
                    #     float(x), float(y), float(w), float(h))


        #image = cvDrawBoxes(drawdetections, frame_resized)
        image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        out.write(image)
        cv2.imshow('Warning-Sys', image)

        key = cv2.waitKey(1) & 0xff

        # Break the loop when Q is pressed
        if key == ord('q'):
            print('Broke the loop\n')
            print("Number of cars: " + str(ot.returncounter()))
            print("Framecount: " + str(framecount))
            break

        # Pauses the loop/video
        if (key == ord('p')):
            cv2.waitKey(-1)

        # print(1/(time.time()-prev_time))
        # print((time.time()-prev_time)))

    cap.release()
    out.release()


if __name__ == "__main__":
    YOLO()
