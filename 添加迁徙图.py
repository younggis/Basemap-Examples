# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:05:06 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


dpi=72

fig = plt.figure(figsize=(1366./2/dpi, 768./2/dpi)) #图片大小，单位为像素16：9。
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0]) #x,y,width,height

#新建地图
map = Basemap(projection='ortho', lat_0=30, lon_0=104)
#绘制海岸线
map.drawcoastlines()

#上海
map.drawgreatcircle(116.41667,39.91667, 121.43333,34.50000,linewidth=2,color='r')
#天津
map.drawgreatcircle(116.41667,39.91667,117.20000,39.13333,linewidth=2,color='g')
#香港
map.drawgreatcircle(116.41667,39.91667, 114.10000,22.20000,linewidth=2,color='b')
#广州
map.drawgreatcircle(116.41667,39.91667, 113.23333,23.16667,linewidth=2,color='g')
#杭州
map.drawgreatcircle(116.41667,39.91667,120.20000,30.26667,linewidth=2,color='r')
#重庆
map.drawgreatcircle(116.41667,39.91667, 106.45000, 29.56667,linewidth=2,color='g')
#乌鲁木齐
map.drawgreatcircle(116.41667,39.91667, 87.68333,43.76667,linewidth=2,color='b')
#拉萨
map.drawgreatcircle(116.41667,39.91667, 91.00000,29.60000,linewidth=2,color='g')
#哈尔滨
map.drawgreatcircle(116.41667,39.91667,126.63333,45.75000,linewidth=2,color='b')

x, y = map.gcpoints(116.41667,39.91667, 40,20, 50)
map.plot(x, y,linewidth=2,color='b')


#显示结果
plt.show()
