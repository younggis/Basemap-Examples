# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:00:19 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#设置投影
#map = Basemap(projection='cyl')
map = Basemap(projection='aeqd', lon_0 = 104, lat_0 = 30)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()

plt.show()