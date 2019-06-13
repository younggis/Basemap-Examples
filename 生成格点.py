# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 21:07:00 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

fig=plt.figure(figsize=(9, 3))

map = Basemap(width=12000000,height=8000000,
            resolution='l',projection='stere',
            lat_ts=50,lat_0=50,lon_0=-107.)

lons, lats, x, y = map.makegrid(30, 30, returnxy=True)

map.scatter(x, y, marker='o')
map.drawcoastlines()


plt.show()