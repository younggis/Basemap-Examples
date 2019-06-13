# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:39:07 2019

@author: Administrator
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from osgeo import gdal
from numpy import linspace
from numpy import meshgrid
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import shapefile

map = Basemap(projection='cyl', 
              lat_0=0, lon_0=0,
              llcrnrlon=85, 
              llcrnrlat=25, 
              urcrnrlon=90, 
              urcrnrlat=30)

#读取tiff
ds = gdal.Open("sample_files/dem/srtm_54_07.img")
data = ds.ReadAsArray()

#在指定的间隔内返回均匀间隔的数字
#params:start开始，end结束，num生成的样本数
x = linspace(0, map.urcrnrx, data.shape[1])
y = linspace(0, map.urcrnry, data.shape[0])

#生成网格点坐标矩阵
xx, yy = meshgrid(x, y)
#等值面
cs=map.contourf(xx, yy, data)

#获取shp geometry
def getShpPath(shpPath):
    try:
        sf=shapefile.Reader(shpPath)
        vertices = []
        codes = []
        for shape_rec in sf.shapeRecords():
            pts = shape_rec.shape.points
            prt = list(shape_rec.shape.parts) + [len(pts)]
            for i in range(len(prt) - 1):
                for j in range(prt[i], prt[i + 1]):
                    vertices.append((pts[j][0], pts[j][1]))
                codes += [Path.MOVETO]
                codes += [Path.LINETO] * (prt[i + 1] - prt[i] - 2)
                codes += [Path.CLOSEPOLY]
            path = Path(vertices, codes)
        return path
    except Exception as err:
        return err
#裁剪
def clipBorder(path):
    if path is not None:
        patch=PathPatch(path,linewidth='2',facecolor='none',edgecolor='#df0029')
    else:
        patch=None
    return patch
path=getShpPath("sample_files/clip.shp")
patch=clipBorder(path);
plt.gca().add_patch(patch)
if patch is not None:
    for collection in cs.collections:
        collection.set_clip_on(True)
        collection.set_clip_path(patch)


plt.show()