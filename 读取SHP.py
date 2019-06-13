# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:49:23 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#新建地图
map = Basemap(llcrnrlon=-0.5,llcrnrlat=39.8,urcrnrlon=4.,urcrnrlat=43.,resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = 1)
#填充海洋颜色 
map.drawmapboundary(fill_color='aqua')
#填充陆地和湖泊颜色
map.fillcontinents(color='coral',lake_color='aqua')
#绘制海岸线
map.drawcoastlines()

#读取shp文件
map.readshapefile('sample_files/comarques', 'comarques')
#显示结果
plt.show()