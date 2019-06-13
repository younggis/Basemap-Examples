# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:21:19 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
#新建地图
map = Basemap()
#绘制海岸线
map.drawcoastlines()


#添加经纬度线
map.drawparallels(np.arange(0,90,3))
map.drawmeridians(np.arange(0,90,3))


#显示结果
plt.show()