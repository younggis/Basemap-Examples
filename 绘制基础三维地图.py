# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:51:33 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#新建地图，’ortho’指正射投影，具体参数后面再讨论；后面两个参数是设置中心点
map = Basemap(projection='ortho', lat_0=0, lon_0=0)

#填充海洋颜色 
map.drawmapboundary(fill_color='aqua')
#填充陆地和湖泊颜色
map.fillcontinents(color='coral',lake_color='aqua')
#绘制海岸线
map.drawcoastlines()

plt.show()