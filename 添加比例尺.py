# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 20:33:16 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon=-10.5,llcrnrlat=35,urcrnrlon=4.,urcrnrlat=44.,
             resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = -3.25)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#cc9955',lake_color='aqua')
map.drawcoastlines()

#lon, lat, lon0, lat0, length, barstyle='simple', units='km', fontsize=9, yoffset=None, labelstyle='simple', fontcolor='k', fillcolor1='w', fillcolor2='k', ax=None, format='%d', zorder=None, linecolor=None, linewidth=None
map.drawmapscale(-7., 35.8, -3.25, 39.5, 500, barstyle='fancy')
map.drawmapscale(-0., 35.8, -3.25, 39.5, 500, fontsize = 14)

plt.show()