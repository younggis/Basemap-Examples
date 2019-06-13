# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:43:17 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from osgeo import gdal
from numpy import linspace
from numpy import meshgrid

map = Basemap(projection='tmerc', 
              lat_0=0, lon_0=3,
              llcrnrlon=1.819757266426611, 
              llcrnrlat=41.583851612359275, 
              urcrnrlon=1.841589961763497, 
              urcrnrlat=41.598674173123)

#读取tiff
ds = gdal.Open("sample_files/dem.tiff")
data = ds.ReadAsArray()

#在指定的间隔内返回均匀间隔的数字
#params:start开始，end结束，num生成的样本数
x = linspace(0, map.urcrnrx, data.shape[1])
y = linspace(0, map.urcrnry, data.shape[0])

#生成网格点坐标矩阵
xx, yy = meshgrid(x, y)

#伪彩图
map.pcolormesh(xx, yy, data)

plt.show()