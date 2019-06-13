# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:25:00 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#新建地图
map = Basemap()
#绘制海岸线
map.drawcoastlines()

#添加多个点
lons = [0, 10, -20, -20]
lats = [0, -10, 40, -20]
x, y = map(lons, lats)
map.scatter(x, y, marker='D',color='m')

#显示结果
plt.show()