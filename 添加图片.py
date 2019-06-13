# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:22:01 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
fig = plt.figure()

map = Basemap(projection='ortho', 
              lat_0=0, lon_0=0)

map.drawlsmask(land_color = "#ddaa66", 
               ocean_color="#7777ff",
               resolution = 'l')

x0, y0 = map(0, 0)
x1, y1 = map(10, 10)

#extent 绘制区域，左下角和右上角点
plt.imshow(plt.imread('sample_files/by.png'),  extent = (x0, x1, y0, y1))
      
#绘制区域，x,y,width,height  
axicon = fig.add_axes([0., 0., 0.15, 0.15])
axicon.imshow(plt.imread('sample_files/by.png'), origin = 'upper')

#清空坐标轴标注
axicon.set_xticks([])
axicon.set_yticks([])

plt.show()