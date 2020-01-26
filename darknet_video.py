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
from pyimagesearch.centroidtracker import CentroidTracker
from collections import OrderedDict
from tkinter import filedialog, Label, Tk, Button, StringVar

framecount = 0


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

# def cvDrawBoxes(detections, img):
#     for counter, detection in enumerate(detections):
#         x, y, w, h = detection[2][0],\
#             detection[2][1],\
#             detection[2][2],\
#             detection[2][3]
#         xmin, ymin, xmax, ymax = convertBack(
#             float(x), float(y), float(w), float(h))
#         pt1 = (xmin, ymin)
#         pt2 = (xmax, ymax)
#         cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
#         cv2.putText(img,
#                     detection[0].decode() +
#                     " [" + str(counter) + " " +
#                     str(round(detection[1] * 100, 2)) + "]",
#                     (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#                     [0, 255, 0], 2)

#     del detections[:]
#     return img


netMain = None
metaMain = None
altNames = None

framecountlist = []

prev_h = OrderedDict()
prev_w = OrderedDict()

cur_h = OrderedDict()
cur_w = OrderedDict()

w_count = 0
start_time = 0
warning_dict = OrderedDict()


def YOLO(videopath):

    global metaMain, netMain, altNames, framecount, cur_h, cur_w, prev_h, prev_w, w_count, warning_dict, start_time

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

    root = Tk()

    window_width = 416
    window_height = 416
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    xcoord = int((screen_width/2) - (window_width/2))
    ycoord = int((screen_height/2) - (window_height/2))

    cap = cv2.VideoCapture(videopath)
    cap.set(3, cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(4, cv2.CAP_PROP_FRAME_WIDTH)

    cv2.namedWindow("Warning-Sys")
    cv2.moveWindow("Warning-Sys", xcoord, ycoord)

    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                       darknet.network_height(netMain), 3)

    ct = CentroidTracker()

    w_count = 0

    while True:
        prev_time = time.time()
        ret, frame_read = cap.read()
        framecount += 1
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

        # print(len(detections)
        rects = []

        for detection in detections:
            x, y, w, h = detection[2][0],\
                detection[2][1],\
                detection[2][2],\
                detection[2][3]
            if(90 < x < 326 and 90 < y < 326):
                if(w > 35 and h > 50 and w < 355):
                    xmin, ymin, xmax, ymax = convertBack(
                        float(x), float(y), float(w), float(h))
                    rects.append((xmin, ymin, xmax, ymax))

        objects = ct.update(rects)

        for (objectID, values) in objects.items():
            # text = "ID {}".format(objectID)
            # cv2.putText(frame_resized, text, (values[0][0] - 10, values[0][1] - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            pt1 = ((values[1][0], values[1][1]))  # x min & y min
            pt2 = ((values[1][2], values[1][3]))  # x max & y max
            # cv2.rectangle(frame_resized, pt1, pt2, (0, 255, 0), 1)
            # cv2.circle(frame_resized,
            #            (values[0][0], values[0][1]), 4, (0, 255, 0), -1)

            w = (pt2[0] - pt1[0])
            h = (pt2[1] - pt1[1])
            # print("W: {}\nH: {}".format(w,h))

            cur_w[objectID] = w
            cur_h[objectID] = h

            if objectID not in prev_w:
                prev_w[objectID] = w
                prev_h[objectID] = h

            else:
                if(start_time == 0):
                        start_time = time.time()

                if(abs(cur_w[objectID] - prev_w[objectID]) * 2.5 > 32 or abs(cur_h[objectID] - prev_h[objectID]) * 2.5 > 35):
                    cv2.rectangle(frame_resized, pt1, pt2, (255, 0, 0), 1)
                    # print("Current W: {}\nCurrent H: {}".format(cur_w[objectID],cur_h[objectID]))
                    # print("Prev W: {}\nPrev H: {}".format(prev_w[objectID],prev_h[objectID]))
                    # print("ROC W: " + str(abs(cur_w[objectID] - prev_w[objectID]) * 2.5) + "\nROC H: "+ str(abs(cur_h[objectID]-prev_h[objectID]) *2.5))
                    # print("Car {} triggered".format(objectID))
                    wave_obj = sa.WaveObject.from_wave_file("bleepsfxwav.wav")
                    play_obj = wave_obj.play()
                    # play_obj.wait_done()
                    if((time.time() - start_time) >= 2):
                        w_count += 1
                        start_time = 0
                        warning_dict[w_count] = framecount

                elif(w > 173 and h > 220):
                    # print("W: {}\nH: {}".format(w,h))
                    wave_obj = sa.WaveObject.from_wave_file("bleepsfxwav.wav")
                    play_obj = wave_obj.play()

                    if((time.time() - start_time) >= 2):
                        w_count += 1
                        start_time = 0
                        warning_dict[w_count] = framecount

                else:
                    cv2.rectangle(frame_resized, pt1, pt2, (0, 255, 0), 1)

                prev_w[objectID] = w
                prev_h[objectID] = h

        image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        cv2.imshow('Warning-Sys', image)

        key = cv2.waitKey(1) & 0xff
        # Break the loop when Q is pressed
        if key == ord('q'):
            print('Broke the loop\n')
            print("Framecount: " + str(framecount))
            break

        # Pauses the loop/video
        if (key == ord('p')):
            cv2.waitKey(-1)

        # print(1/(time.time()-prev_time))
        # print((time.time()-prev_time)))
    cap.release()
    root.destroy()
    cv2.destroyWindow('Warning-Sys')

    cur_w.clear()
    cur_h.clear()
    prev_w.clear()
    prev_h.clear()
    del rects[:]


if __name__ == "__main__":
    YOLO()
