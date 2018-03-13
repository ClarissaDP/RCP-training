#!/usr/bin/env python

# Dilation and Erosion modules

import cv2
import numpy as np


def dilation(img, k):
    kernel = np.ones((k,k),np.uint8)
    dilation = cv2.dilate(img, kernel,iterations = 7)
    return dilation


def erosion(img, k):
    kernel = np.ones((k,k),np.uint8)
    erosion = cv2.erode(img, kernel,iterations = 7)
    return erosion
