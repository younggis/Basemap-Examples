# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:05 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#新建地图
map = Basemap(projection='aeqd', lon_0 = 10, lat_0 = 50)
#绘制海岸线
map.drawcoastlines()

#经纬度转平面坐标
print map(10, 50)

#平面坐标转经纬度
print map(20015077.3712, 20015077.3712, inverse=True)

#显示结果
plt.show()