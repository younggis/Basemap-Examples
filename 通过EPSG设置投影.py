# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:02:08 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#通过epsg设置投影
#llcrnrlon左边经度
#llcrnrlat下边纬度
#urcrnrlon右边经度
#urcrnrlat上边纬度
map = Basemap(llcrnrlon=60,llcrnrlat=0,urcrnrlon=120,urcrnrlat=60, resolution = 'h', epsg=3857)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()
plt.show()