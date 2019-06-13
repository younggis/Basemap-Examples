# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:11:57 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import shiftgrid
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np

map = Basemap(projection='tmerc', 
              lat_0=0, lon_0=3,
              llcrnrlon=1.819757266426611, 
              llcrnrlat=41.583851612359275, 
              urcrnrlon=1.841589961763497, 
              urcrnrlat=41.598674173123)

ds = gdal.Open("sample_files/dem.tiff")
elevation = ds.ReadAsArray()

#添加图像，图像可以是常规的RGB图像，也可以是用CMAP着色的字段
#添加图像
#imread 读取图片
map.imshow(plt.imread('sample_files/orthophoto.jpg'))
#添加地形
map.imshow(elevation, cmap = plt.get_cmap('terrain'), alpha = 0.8)

plt.show()