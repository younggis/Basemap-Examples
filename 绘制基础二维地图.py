# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:24:49 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#新建地图
map = Basemap()
#绘制海岸线
map.drawcoastlines()

#显示结果
plt.show()

#保存到本地
#plt.savefig('test.png')