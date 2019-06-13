# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:39:40 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


map = Basemap()

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()

#创建带有指示兴趣点的箭头的文本
x, y = map(2, 41)
x2, y2 = map(-90, 10)
plt.annotate('Barcelona', xy=(x, y),  xycoords='data',
                xytext=(x2, y2), textcoords='offset points',
                color='r',fontsize=14,
                arrowprops=dict(arrowstyle="fancy", color='b'))
x3, y3 = map(104, 30)
plt.annotate('Barcelona', xy=(x, y),  xycoords='data',
                xytext=(x3, y3), textcoords='data',fontsize=14,
                arrowprops=dict(arrowstyle="->"))


#在地图上绘制文本
x4, y4 = map(2, 10)
plt.text(x4, y4, 'Lagos',fontsize=12,fontweight='bold',
                    ha='left',va='bottom',color='w')
x5, y5 = map(2, -10)
plt.text(x5, y5, 'Barcelona',fontsize=12,fontweight='bold',
                    ha='left',va='center',color='w',
                    bbox=dict(facecolor='b', alpha=0.2))
plt.show()