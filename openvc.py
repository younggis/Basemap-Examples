# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:45:43 2019

@author: Administrator
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('I:\Lena.jpg',0)
edges = cv2.Canny(img, 100, 200)

cv2.imshow('Edges',edges)
cv2.waitKey(0)