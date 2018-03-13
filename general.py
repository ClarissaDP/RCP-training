#!/usr/bin/env python

# General libraries
import numpy as np
import cv2
import sys, os
import argparse
import time
import imutils
import copy as cp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



# -------------------- #
out_path = "../outputs_rcp/"
out_image = "image_frames/"
out_video = "videos/"
# -------------------- #

# -------- ploting globals -------- #
fig = plt.figure()
min_y = 100; max_y = 200
ax = plt.axes(xlim=(0,60), ylim=(min_y, max_y))
line, = ax.plot([], [], animated=True)
# --------------------------------- #


# -------- globals settings -------- #

# setting variables
y_diff_min = 2
y_diff_max = 80
x_diff_max = 90 # check if is not doing CPR anymore (ventilation...)
first_event = True
speed_conv = 1  # check need
second_time = 0
buff = 0
end_y = 0
travel_count = 0
previous_travel = "D2U"
travel = {'up': 0, 'down': 1}

# ---------------------------------- #



def output(name, out, i):
    output_name = out_path + out_image + name + "_" + str(i) + ".png"
    cv2.imwrite(output_name, out)
    # print output_name

def setup():
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    if not os.path.exists(out_path + out_image):
        os.makedirs(out_path + out_image)

    if not os.path.exists(out_path + out_video):
        os.makedirs(out_path + out_video)


def set_color(color, color_type):
    if (color_type == 'BGR' and color == 'yellow'):
        return yellow_BGR()
    else:
        print("Color not defined")
        return (-1)

def yellow_BGR():
    # define range of yellow color in BGR
    lower = np.array([0, 100, 100])
    upper = np.array([20, 255, 255])
    return (lower, upper)

def red_HSV():
    # red color in HSV
    lower = np.array([169, 100, 100])
    upper = np.array([189, 255, 255])
    return (lower, upper)

def red_BGR():
    # red color in BGR
    lower = np.array([0, 0, 200])
    upper = np.array([20, 20, 255])
    return (lower, upper)


def largest_contour(contours, mask, res):
    height, width = mask.shape
    min_x, min_y = width, height
    max_x = max_y = 0
    largest_area = 0
    x, y, w, h = 0, 0, 0, 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if (area > largest_area):
            largest_area = area
            (x,y,w,h) = cv2.boundingRect(contour)

    if ( x and y and w and h ):
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)

        if max_x - min_x > 0 and max_y - min_y > 0:
            cv2.rectangle(res, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
    else:
        cv2.putText(res, "Marker not found", (30,50), cv2.FONT_HERSHEY_TRIPLEX, 1, 255)

    return (res, min_x, min_y)


def display(k_mask, res, to_show, to_print, to_video):
    # Display the resulting frame
    if (to_show):
        cv2.imshow('mask', k_mask)
        cv2.namedWindow('Resultado', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Resultado', screen_width, screen_height)
        cv2.imshow('Resultado', res)
        time.sleep(0.5)
    if (to_print):
        output("mask", k_mask, i)
        output("res", res, i)


def grab_frame(frame):
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)


