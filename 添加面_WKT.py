# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:29:11 2019

@author: Administrator
"""

#导入包
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

dpi=72

fig = plt.figure(figsize=(1366./2/dpi, 768./2/dpi)) #图片大小，单位为像素16：9。
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0]) #x,y,width,height

#新建地图
map = Basemap(resolution='l', area_thresh=10000, projection='cyl', llcrnrlon=-180, urcrnrlon=180, llcrnrlat=-90, urcrnrlat=90)
#绘制海岸线
map.drawcoastlines()

#格式化wkt,构造patch    
def formateWKT(wktstr,fillcolor):
    try:
        wkt=wktstr.replace("POLYGON ((","").replace("))","")
        points=wkt.split(',')
        patches= []
        path=[]
        for index in range(len(points)):
            point=points[index].split(' ')
            p=[]
            p.append(float(point[0]))
            p.append(float(point[1]))
            path.append(p)
        patches.append(Polygon(path, True))
        patchcollection=PatchCollection(patches, facecolor= fillcolor, edgecolor=fillcolor, linewidths=1., zorder=2,alpha=0.8)
        return patchcollection
    except Exception as err:
        return err
patchcollection=formateWKT('POLYGON ((0 0,40 0,40 20,0 20,0 0))','b')
ax.add_collection(patchcollection)

#显示结果
plt.show()

#保存到本地
#plt.savefig('test.png')


