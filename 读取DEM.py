# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:54:40 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from osgeo import gdal

map = Basemap(projection='cyl', 
              lat_0=0, lon_0=0,
              llcrnrlon=85, 
              llcrnrlat=25, 
              urcrnrlon=90, 
              urcrnrlat=30)

#读取tiff
ds = gdal.Open("sample_files/dem/srtm_54_07.img")
data = ds.ReadAsArray()

map.imshow(data, cmap = plt.get_cmap('terrain'), alpha = 0.5)

plt.show()