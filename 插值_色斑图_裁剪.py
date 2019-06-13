# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 16:19:06 2019

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
import numpy as np 
import math

class IDW:
    def __init__(self,extent,noData):
        self.extent=extent #插值范围
        self.noData=noData #过滤无效值
        self.xNum=0 #纵向分段数量
        self.yNum=0 #横向分段数量
        self.xMin=0
        self.xMax=0
        self.yMin=0
        self.yMax=0
        self.xx=[]
        self.yy=[]
        self.gridPoints=self.extentComputer()
    #idw算法
    def Interpolation(self,samplePoints):
        if len(samplePoints) < 3:
            return self.gridPoints
    
        m1=len(self.gridPoints)
        #过滤nodata值
        tempPoints = []
        for i in range(len(samplePoints)):
            if samplePoints[i][2]==self.noData:
                continue
            tempPoints.append(samplePoints[i])
        samplePoints=tempPoints
    
        m0=len(samplePoints)
        #反距离列表
        r=[]
        for i in range(m1):
            for j in range(m0):
                tmpDis=math.sqrt(pow(self.gridPoints[i][0] - samplePoints[j][0], 2)+pow(self.gridPoints[i][1] - samplePoints[j][1], 2))
                r.append(tmpDis)
        #插值函数
        for i in range(m1):
            #查找重复
            ifFind = False
            for j in range(m0*i,m0*i+m0):
                if abs(r[j])<0.0001:
                    self.gridPoints[i].append(samplePoints[j - m0 * i][2])
                    ifFind = True
                    break
            if ifFind==True:
                continue
            numerator = 0
            denominator = 0
            for j in range(m0 * i,m0 * i + m0):
                numerator += samplePoints[j - m0 * i][2] / (r[j] * r[j])
                denominator += 1 / (r[j] * r[j])
            self.gridPoints[i].append(numerator / denominator)
        return self.gridPoints

    #计算格网
    def extentComputer(self):
        extent=self.extent
        cellSize = self.cellSizeComputer(extent)
        yNum = int(math.ceil((extent[3] - extent[1]) / cellSize))
        xNum = int(math.ceil((extent[2] - extent[0]) / cellSize))
        self.xNum=xNum+2
        self.yNum=yNum+2
        
        self.xMin=extent[0]-cellSize
        self.xMax=extent[0]+cellSize*xNum
        self.yMin=extent[1]-cellSize
        self.yMax=extent[1]+cellSize*yNum
        
        grids = []
        for i in range(-1,xNum + 1):
            for j in range(-1,yNum + 1):
                grids.append([extent[0] + cellSize * i, extent[1] + cellSize * j])
        for i in range(-1,xNum + 1):
            self.xx.append(extent[0] + cellSize * i)
        for j in range(-1,yNum + 1):
            self.yy.append(extent[1] + cellSize * j)
        return grids
    #计算像元大小
    def cellSizeComputer(self,extent):
        height = extent[3] - extent[1]
        length = extent[2] - extent[0]
        cellSize = 0.0001
        if length>=height:
            cellSize=round(length/float(200),4)
        else :
            cellSize=round(height/float(200),4)
        if cellSize<0.0001:
            cellSize=0.0001
        return cellSize

    #查找某一个点的插值后值
    def findValue(self,point):
        cellSize = self.cellSizeComputer(self.extent)
        yInterval=int(math.floor((point[1]-self.extent[1])/cellSize))+2
        xInterval=int(math.floor((point[0]-self.extent[0])/cellSize))+2
        index=xInterval*self.yNum+yInterval
        return self.gridPoints[index]
    
samplePoints = [
	[95.820041, 28.939994, 2.3],
	[88.637541, 28.927494, 5.4],
	[87.167541, 28.629161, 0.4],
	[95.839208, 30.991661, 6.8],
	[94.123374, 30.553328, 3.1],
	[89.267541, 29.740828, 6.2],
	[89.594181, 28.682597, 7.6],
	[97.698374, 30.666661, 1.2],
	[95.268498, 32.201917, 2.3],
	[87.190041, 29.118328, 4.6],
	[90.175850, 29.387233, 7.8],
	[97.093374, 31.186661, 2.1],
	[88.728374, 31.154161, 0.4],
	[85.977541, 31.839994, 5.4],
	[96.567541, 31.243328, 7.6],
	[88.397541, 28.283952, 3.4],
	[93.336708, 29.740828, 4.6],
	[87.667908, 29.954285, 8.7],
	[92.174739, 28.463913, 7.6],
	[97.146708, 30.040828, 7.6],
	[91.672541, 27.524161, 8.8],
	[88.726942, 30.538296, 2.3],
	[85.008374, 29.637494, 4.5],
	[96.614208, 28.988328, 6.7],
	[98.027541, 30.414994, 8.7],
	[91.747541, 29.840828, 4.5],
	[85.798374, 28.747494, 6.3],
	[80.142541, 32.466661, 2.1],
	[95.727456, 28.630249, 3.4],
	[95.613188, 30.055957, 1.8],
	[90.962541, 30.389994, 0.2],
	[93.892541, 29.066661, 4.2]
]
idw=IDW([78.393604,26.8529,99.109761,36.485277],999999)
interData=idw.Interpolation(samplePoints)


dataList=[]
for i in range(idw.yNum):
    dataList.append([])
    for j in range(idw.xNum):
        dataList[i].append(interData[int(j*idw.yNum)+i][2])
        
base_map = Basemap(resolution='l', area_thresh=10000, projection='cyl',
              llcrnrlon=idw.xMin, 
              llcrnrlat=idw.yMin, 
              urcrnrlon=idw.xMax, 
              urcrnrlat=idw.yMax)
xx, yy = meshgrid(idw.xx, idw.yy)
cs=base_map.contourf(xx, yy, dataList)

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
        patch=PathPatch(path,linewidth='0',facecolor='none',edgecolor='none',alpha=0.2)
    else:
        patch=None
    return patch
path=getShpPath("sample_files/t_area_province_geo.shp")
patch=clipBorder(path);
plt.gca().add_patch(patch)
if patch is not None:
    for collection in cs.collections:
        collection.set_clip_on(True)
        collection.set_clip_path(patch)
#隐藏轴
plt.axis('off')
plt.show()