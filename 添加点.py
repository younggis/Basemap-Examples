# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:24:00 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#新建地图
map = Basemap()
#绘制海岸线
map.drawcoastlines()

#添加点
x, y = map(104, 30)
map.plot(x, y, marker='D',color='m')

#显示结果
plt.show()