# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:56:17 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from numpy import array
from numpy import max


map = Basemap(llcrnrlon=-0.5,llcrnrlat=39.8,urcrnrlon=4.,urcrnrlat=43.,
             resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = 1)


map.readshapefile('sample_files/lightnings', 'lightnings')

x = []
y = []
c = []

for info, lightning in zip(map.lightnings_info, map.lightnings):
    x.append(lightning[0])
    y.append(lightning[1])
    
    if float(info['amplitude']) < 0:
        c.append(-1 * float(info['amplitude']))
    else:
        c.append(float(info['amplitude']))
    
plt.figure(0)

map.drawcoastlines()
map.readshapefile('sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y))

map.colorbar(location='bottom')



plt.figure(1)

map.drawcoastlines()
map.readshapefile('sample_files/comarques', 'comarques')

#gridsize越大，格点越小
#mincnt代表一个格点的最少数量，若为0，则全图都会填充
map.hexbin(array(x), array(y), gridsize=20, mincnt=0, cmap='summer', bins='log')

map.colorbar(location='bottom', format='%.1f', label='log(# lightnings)')



plt.figure(2)

map.drawcoastlines()
map.readshapefile('sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y), gridsize=20, mincnt=1, cmap='summer', norm=colors.LogNorm())

cb = map.colorbar(location='bottom', format='%d', label='# lightnings')

cb.set_ticks([1, 5, 10, 15, 20, 25, 30])
cb.set_ticklabels([1, 5, 10, 15, 20, 25, 30])




plt.figure(3)

map.drawcoastlines()
map.readshapefile('sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y), C = array(c), reduce_C_function = max, gridsize=20, mincnt=1, cmap='YlOrBr', linewidths=0.5, edgecolors='k')

map.colorbar(location='bottom', label='Mean amplitude (kA)')


plt.show()