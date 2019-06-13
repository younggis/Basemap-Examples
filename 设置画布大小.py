# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:33:47 2019

@author: Administrator
"""

import matplotlib.pyplot as plt

# load the image
img = plt.imread('images/image.jpg')

# get the dimensions
ypixels, xpixels, bands = img.shape

# get the size in inches
dpi = 144.
xinch = xpixels / dpi
yinch = ypixels / dpi

# plot and save in the same size as the original
fig = plt.figure(figsize=(xinch,yinch))

ax = plt.axes([0., 0., 1., 1.], frameon=False, xticks=[],yticks=[])


ax.imshow(img, interpolation='none')

plt.savefig('logo.png', dpi=dpi, transparent=True)