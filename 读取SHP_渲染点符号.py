# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:56:12 2019

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

#读取shp
lightning_info = map.readshapefile('sample_files/lightnings', 'lightnings')

#根据字段属性设置点符号
#函数用于将可迭代对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象。
for info, lightning in zip(map.lightnings_info, map.lightnings):
    if float(info['amplitude']) < 0:
        marker = '_'
    else:
        marker = '+'
    map.plot(lightning[0], lightning[1], marker=marker, color='m', markersize=8, markeredgewidth=2)
    
#显示结果
plt.show()