# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:17:21 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np

fig     = plt.figure()
ax      = fig.add_subplot(111)

map = Basemap(llcrnrlon=-0.5,llcrnrlat=39.8,urcrnrlon=4.,urcrnrlat=43.,
             resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = 1)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#ddaa66',lake_color='aqua')
map.drawcoastlines()

map.readshapefile('sample_files/comarques', 'comarques', drawbounds = False)

patches   = []

for info, shape in zip(map.comarques_info, map.comarques):
    if info['nombre'] == 'Selva':
        patches.append( Polygon(np.array(shape), True) )
        
        #通过点序列连线绘制面，无填充
        x, y = zip(*shape) 
        map.plot(x, y, marker=None,color='m')
#绘制面       
ax.add_collection(PatchCollection(patches, facecolor= 'm', edgecolor='k', linewidths=1., zorder=2))

plt.show()