# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:05:17 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt

#设置地图范围
#llcrnrlon左边经度
#llcrnrlat下边纬度
#urcrnrlon右边经度
#urcrnrlat上边纬度
#map = Basemap(llcrnrlon=100,llcrnrlat=20,urcrnrlon=120,urcrnrlat=60, resolution = 'c', projection = 'merc')

#llcrnrx最小x
#llcrnry最小y
#urcrnrx最大x
#urcrnry最大y
#map = Basemap(llcrnrx=500000.,llcrnry=500000.,urcrnrx=2700000.,urcrnry=2700000, resolution = 'c', epsg = 3857)

#width宽
#height高
#lon_0中心点的经度
#lat_0中心点的纬度
map = Basemap(projection='aeqd',lon_0 = 0,lat_0 = 0, width = 10000000,height = 10000000)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')

map.drawcoastlines()
plt.show()