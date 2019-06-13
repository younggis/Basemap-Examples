# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:29:47 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#新建地图
map = Basemap()
#绘制海岸线
map.drawcoastlines()

lons = [-10, -20, -25, -10, 0, 10]
lats = [40, 30, 10, 0, 0, -5]

x, y = map(lons, lats)
map.plot(x, y, marker=None,color='m')

#显示结果
plt.show()

#保存到本地
#plt.savefig('test.png')