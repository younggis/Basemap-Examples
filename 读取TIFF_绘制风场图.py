# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:24:49 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np


map = Basemap(llcrnrlon=-93.7, llcrnrlat=28., urcrnrlon=-66.1, urcrnrlat=39.5,
              projection='lcc', lat_1=30., lat_2=60., lat_0=34.83158, lon_0=-98.)

#读取tiff
ds = gdal.Open("sample_files/wrf.tiff")
lons = ds.GetRasterBand(4).ReadAsArray()
lats = ds.GetRasterBand(5).ReadAsArray()
u10 = ds.GetRasterBand(1).ReadAsArray()
v10 = ds.GetRasterBand(2).ReadAsArray()

x, y = map(lons, lats)

#在指定的间隔内返回均匀间隔的数字
#params:start开始，end结束，num生成的样本数
yy = np.arange(0, y.shape[0], 4)
xx = np.arange(0, x.shape[1], 4)
#生成网格点坐标矩阵
points = np.meshgrid(yy, xx)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#cc9955', lake_color='aqua', zorder = 0)
map.drawcoastlines(color = '0.15')

#绘制风场
map.barbs(x[points], y[points], u10[points], v10[points], 
    pivot='middle', barbcolor='#333333')


plt.show()