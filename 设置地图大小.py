# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:33:47 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#新建地图
map = Basemap()

dpi=72

fig = plt.figure(figsize=(1366./dpi, 768./dpi)) #图片大小，单位为像素16：9。
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0]) #x,y,width,height

#绘制海岸线
map.drawcoastlines()

plt.savefig('test.png',dpi=dpi,transparent=True)