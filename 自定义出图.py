# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:57:47 2020

@author: Administrator
"""

import io
import time
import pymssql
import psycopg2
import zipfile
import os,shutil
import sys
import gc
import re
import math
from PIL import Image

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
	
from datetime import datetime
import logging
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt = DATE_FORMAT ,filename=r"log.log")

try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr
    import osr




earth_radius = 20037508.342789244
base_path='D:\\root\\web\\diggeomanage\\download\\'
template_path='D:\\python\\template\\'
download_path='http://10.110.39.173:8080/diggeomanage/download/'


#查询数据
def getTableData(sql):
    conn = pymssql.connect("10.110.39.193", "sa", "SCGX_2018", "Data_Center",charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    recordRows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return recordRows
#查询postgresql数据
def getPGTableData(sql):
    conn = psycopg2.connect(database="postgis", user="postgres", password="postgis", host="10.110.39.222", port="5432")
    cur = conn.cursor()
    cur.execute(sql)
    recordRows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return recordRows
#插入下载的url
def updateStatusAndURL(_id,url):
    conn = pymssql.connect("10.110.39.193", "sa", "SCGX_2018", "Data_Center",charset='utf8')
    cur = conn.cursor()
    cur.execute(u"update t_gis_download_manage set status=2,url='"+url+"' where id="+str(_id))
    conn.commit()
    cur.close()
    conn.close()
#插入短信
def inertInfo(phone,content):
    conn = pymssql.connect("10.110.39.193", "sa", "SCGX_2018", "Data_Center",charset='utf8')
    cur = conn.cursor()
    cur.executemany("insert into sms_list(mobile,content) values(%s,%s);",[(phone, content)])
    conn.commit()
    cur.close()
    conn.close()
#组装sql
def createSQL(table,city,county,branch):
    sql=''
    if table=='1':
        if city=='' or city==None:
            city='1=1'
        else:
            city=u"地市='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county=u"区县='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="branch_name='"+branch+"'"
        sql=u"select 新物业唯一 as code,地市 as city,区县 as county,branch_name as branch,新物业名 as name,address,type,面积 as area,中心经度 as lon,中心纬度 as lat,build_num,is_2772,code_2772,is_park,park_num,wkt from t_gis_juminqu_manage where status =1 and "+city+" and "+county+" and "+branch+";"                                           
    if table=='2':
        if city=='' or city==None:
            city='1=1'
        else:
            city="city_name='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="county_name='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="branch_name='"+branch+"'"
        sql=u'select name,address,floor,height,area,建筑物 as code,code_wuyedian,centroidx as lon,centroidy as lat,city_name,county_name,branch_name,is_elevator,elevator_num,is_park,park_floor_num,wkt from t_gis_building_manage where status=1 and '+city+' and '+county+' and '+branch+';' 
    if table=='3':
        if city=='' or city==None:
            city='1=1'
        else:
            city="city='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="county='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="branch_name='"+branch+"'"
        sql='select code,city,county,branch_name,name,lon,lat,datasource,lianluyusu,area,wkt from t_gis_zirancun_manage where status=1 and '+city+' and '+county+' and '+branch+';' 
    if table=='4':
        if city=='' or city==None:
            city='1=1'
        else:
            city="city='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="county='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="branches_name='"+branch+"'"
        sql='select gridId,city,county,grid_name,company_name,branches_name,wkt from t_gis_grid_manage where '+city+' and '+county+' and '+branch+';' 
    if table=='5':
        if city=='' or city==None:
            city='1=1'
        else:
            city="city='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="county='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="branch='"+branch+"'"
        sql='select code,scene_name,fugai_name,code_wuyedian,city,county,branch,scene_type,scene_name2,lon,lat,wkt from t_gis_scene_manage where '+city+' and '+county+' and '+branch+';' 
    if table=='6':
        if city=='' or city==None:
            city='1=1'
        else:
            city="city='"+city+"'"
        sql='select city,unit_type,unit_name,unit_code,unit_person,unit_phone,lon,lat,wkt from t_gis_custom where status=1 and '+city+';' 
    if table=='7':
        if city=='' or city==None:
            city='1=1'
        else:
            city="b.city='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="b.county='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="b.branch_name='"+branch+"'"
        sql='select a.id,case when a.yd_rate>= 0.9 then 1 when a.yd_rate<= 0.5 then 2 when a.dx_rate is null then 4 when a.yd_rate between 0.5 and 0.9 and a.dx_rate-a.yd_rate > 0.05 then 2 when a.yd_rate between 0.5 and 0.9 and a.yd_rate-a.dx_rate > 0.05 then 1 when a.yd_rate between 0.5 and 0.9 then 3 else 4 end jingdui,b.name,st_astext(ST_GeometryN(b.geom,1)) as wkt from zirancun b left join zirancun_summary a on a.id=b.id where a.part_time=(select max(part_time) from zirancun_summary) and '+city+' and '+county+' and '+branch+';' 
    if table=='8':
        if city=='' or city==None:
            city='1=1'
        else:
            city="r.地市='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="r.区县='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="r.branch_name='"+branch+"'"
        sql='select m.a02,case when m.a14=\'劣于竞对\' then 2 when m.a14=\'优于竞对\' then 1 when m.a14=\'持平竞对\' then 3 else 4 end jingdui,m.a03,r.wkt from T_GIS_JUMINQU r left join tdl_market_reside m on m.a02 = r.新物业唯一 where m.stat_date=(select max(stat_date) from tdl_market_reside) and '+city+' and '+county+' and '+branch+';' 
    if table=='9':
        if city=='' or city==None:
            city='1=1'
        else:
            city="b.city_name='"+city+"'"
        if county=='' or county==None:
            county='1=1'
        else:
            county="b.county_name='"+county+"'"
        if branch=='' or branch==None:
            branch='1=1'
        else:
            branch="b.branch_name='"+branch+"'"
        sql='select b.建筑物 id,case when replace(replace(p.p053,char(13),\'\'),char(10),\'\') = \'优势居民区\' then 1 when replace(replace(p.p053,char(13),\'\'),char(10),\'\') = \'劣势居民区\' then 3 when replace(replace(p.p053,char(13),\'\'),char(10),\'\') = \'持平居民区\' then 2 else 0 end p053,b.name,b.wkt from T_GIS_BUILDING b left join view_province_building p on p.building_id = b.建筑物 where 1=1 and '+city+' and '+county+' and '+branch+';' 
    
    return sql
#获取未解析的下载请求
def getUnResolving():
    rows=getTableData('select id,table_name,city,county,branch,create_person from t_gis_download_manage where status=1;')
    for row in rows:
        writeToTAB(row[0],row[1],row[2],row[3],row[4],row[5])
#获取字段
def getFields(table):
    if table=='1':
        fields=fields01
    if table=='2':
        fields=fields02
    if table=='3':
        fields=fields03
    if table=='4':
        fields=fields04
    if table=='5':
        fields=fields05
    if table=='6':
        fields=fields06
    return fields
 


#定义图层字段     
fields01=[{
    'name':'code',
    'label':u'物业点ID',
    'field_type':'s',
    'field_length':20
},{
    'name':'city',
    'label':u'地市',
    'field_type':'s',
    'field_length':20
},{
    'name':'county',
    'label':u'区县',
    'field_type':'s',
    'field_length':20
},{
    'name':'branch',
    'label':u'支局',
    'field_type':'s',
    'field_length':50
},{
    'name':'name',
    'label':u'物业点名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'address',
    'label':u'地址',
    'field_type':'s',
    'field_length':50
},{
    'name':'type',
    'label':u'类型',
    'field_type':'s',
    'field_length':20
},{
    'name':'area',
    'label':u'面积',
    'field_type':'f',
    'field_length':0
},{
    'name':'lon',
    'label':u'中心经度',
    'field_type':'f',
    'field_length':0
},{
    'name':'lat',
    'label':u'中心纬度',
    'field_type':'f',
    'field_length':0
},{
    'name':'build_num',
    'label':u'楼栋数',
    'field_type':'i',
    'field_length':0
},{
    'name':'is_2772',
    'label':u'专项打标',
    'field_type':'s',
    'field_length':20
},{
    'name':'code_2772',
    'label':u'专项标识',
    'field_type':'s',
    'field_length':50
},{
    'name':'is_park',
    'label':u'是否有地下停车场',
    'field_type':'s',
    'field_length':20
},{
    'name':'park_num',
    'label':u'停车场数据量',
    'field_type':'i',
    'field_length':0
}]
    
fields02=[{
    'name':'name',
    'label':u'楼宇名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'address',
    'label':u'地址',
    'field_type':'s',
    'field_length':50
},{
    'name':'floor',
    'label':u'楼层数',
    'field_type':'i',
    'field_length':0
},{
    'name':'height',
    'label':u'楼高',
    'field_type':'i',
    'field_length':0
},{
    'name':'area',
    'label':u'面积',
    'field_type':'f',
    'field_length':0
},{
    'name':'code',
    'label':u'楼宇编码',
    'field_type':'s',
    'field_length':50
},{
    'name':'code_wuyedian',
    'label':u'物业点编号',
    'field_type':'s',
    'field_length':20
},{
    'name':'lon',
    'label':u'中心经度',
    'field_type':'f',
    'field_length':0
},{
    'name':'lat',
    'label':u'中心纬度',
    'field_type':'f',
    'field_length':0
},{
    'name':'city_name',
    'label':u'地市',
    'field_type':'s',
    'field_length':20
},{
    'name':'county_name',
    'label':u'区县',
    'field_type':'s',
    'field_length':20
},{
    'name':'branch_name',
    'label':u'支局',
    'field_type':'s',
    'field_length':50
},{
    'name':'is_elevator',
    'label':u'是否有电梯',
    'field_type':'s',
    'field_length':10
},{
    'name':'elevator_num',
    'label':u'电梯数量',
    'field_type':'i',
    'field_length':0
},{
    'name':'is_park',
    'label':u'是否有地下停车场',
    'field_type':'s',
    'field_length':10
},{
    'name':'park_floor_num',
    'label':u'停车场层数',
    'field_type':'i',
    'field_length':0
}]
       
fields03=[{
    'name':'code',
    'label':u'自然村编码',
    'field_type':'s',
    'field_length':50
},{
    'name':'city',
    'label':u'地市',
    'field_type':'s',
    'field_length':20
},{
    'name':'county',
    'label':u'区县',
    'field_type':'s',
    'field_length':20
},{
    'name':'branch_name',
    'label':u'支局',
    'field_type':'s',
    'field_length':50
},{
    'name':'name',
    'label':u'自然村名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'lon',
    'label':u'中心经度',
    'field_type':'f',
    'field_length':0
},{
    'name':'lat',
    'label':u'中心纬度',
    'field_type':'f',
    'field_length':0
},{
    'name':'datasource',
    'label':u'数据来源',
    'field_type':'s',
    'field_length':50
},{
    'name':'lianluyusu',
    'label':u'覆盖情况',
    'field_type':'s',
    'field_length':50
},{
    'name':'area',
    'label':u'面积',
    'field_type':'f',
    'field_length':0
}]
       
fields04=[{
    'name':'gridId',
    'label':u'网格ID',
    'field_type':'s',
    'field_length':50
},{
    'name':'city',
    'label':u'地市',
    'field_type':'s',
    'field_length':20
},{
    'name':'county',
    'label':u'区县',
    'field_type':'s',
    'field_length':20
},{
    'name':'branches_name',
    'label':u'支局',
    'field_type':'s',
    'field_length':50
},{
    'name':'grid_name',
    'label':u'网格名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'company_name',
    'label':u'分公司',
    'field_type':'s',
    'field_length':50
}]
    
fields05=[{
    'name':'code',
    'label':u'序号',
    'field_type':'s',
    'field_length':20
},{
    'name':'scene_name',
    'label':u'场景组场景名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'fugai_name',
    'label':u'覆盖组场景名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'code_wuyedian',
    'label':u'对应覆盖组物业点ID',
    'field_type':'s',
    'field_length':20
},{
    'name':'city',
    'label':u'地市',
    'field_type':'s',
    'field_length':20
},{
    'name':'county',
    'label':u'区县',
    'field_type':'s',
    'field_length':20
},{
    'name':'branch',
    'label':u'支局',
    'field_type':'s',
    'field_length':50
},{
    'name':'scene_type',
    'label':u'场景分类',
    'field_type':'s',
    'field_length':20
},{
    'name':'scene_name2',
    'label':u'场景名称2',
    'field_type':'s',
    'field_length':50
},{
    'name':'lon',
    'label':u'中心经度',
    'field_type':'f',
    'field_length':0
},{
    'name':'lat',
    'label':u'中心纬度',
    'field_type':'f',
    'field_length':0
}]
fields06=[{
    'name':'city',
    'label':u'地市',
    'field_type':'s',
    'field_length':20
},{
    'name':'unit_type',
    'label':u'单位属性',
    'field_type':'s',
    'field_length':20
},{
    'name':'unit_name',
    'label':u'单位名称',
    'field_type':'s',
    'field_length':50
},{
    'name':'unit_code',
    'label':u'单位编码',
    'field_type':'s',
    'field_length':50
},{
    'name':'unit_person',
    'label':u'客户经理',
    'field_type':'s',
    'field_length':50
},{
    'name':'unit_phone',
    'label':u'客户电话',
    'field_type':'s',
    'field_length':20
},{
    'name':'lon',
    'label':u'中心经度',
    'field_type':'f',
    'field_length':0
},{
    'name':'lat',
    'label':u'中心纬度',
    'field_type':'f',
    'field_length':0
}]

def zipDir(dirpath,outFullName,name):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName,"a",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')
        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(name+fpath,filename))
    zip.close()
    shutil.rmtree(dirpath)
#计算wkt范围
def extentByWKT(wktstr):
    try:
        polygon=wktstr.replace("))","").split("), (")
        wkt=polygon[0]
        if wkt.find("POLYGON ((")>-1:
            wkt=polygon[0].replace("POLYGON ((","").replace(", ",",")
        elif wkt.find("POLYGON((")>-1:
            wkt=polygon[0].replace("POLYGON((","")
        points=wkt.split(',')

        xarray=[]
        yarray=[]
        for index in range(len(points)):
            point=points[index].split(' ')
            xarray.append(float(point[0]))
            yarray.append(float(point[1]))
        
        return [min(xarray),min(yarray),max(xarray),max(yarray)]
    except Exception as err:
        return [78.393604-1,99.109761+1,26.8529-1,36.485277+1]
def millerToXY(lon,lat):
    x =  lon*20037508.342789/180
    y =math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
    y = y *20037508.34789/180
    return [x,y]
#格式化wkt,构造patch    
def createPatches(map,wkt):
    polygon=wkt.replace("))","").split("), (")
    wkt=polygon[0]
    if wkt.find("POLYGON ((") > -1:
        wkt=polygon[0].replace("POLYGON ((","").replace(", ",",")
    elif wkt.find("POLYGON((") > -1:
        wkt=polygon[0].replace("POLYGON((","")
    points=wkt.split(',')
    patches= []
    path=[]
    for index in range(len(points)):
        point=points[index].split(' ')
        p=[]
        coordinates=map(float(point[0]), float(point[1]))
        p.append(coordinates[0])
        p.append(coordinates[1])
        path.append(p)
    patches.append(Polygon(path, True))
    return patches
def calcLevel(extent,elewidth,eleheight):
    width=eleheight
    xystep=extent[3]-extent[1]
    if elewidth>eleheight:
        width=elewidth
        xystep=extent[2]-extent[0]
    resolution=(earth_radius/256)/(xystep/width)
    return int(math.floor(math.log(resolution)/math.log(2))+2)
def xyzToRowCol(x,y,zoom):
    tileNum=math.pow(2,zoom)
    row = math.floor((x + earth_radius) / (earth_radius * 2 / tileNum))
    col = math.floor((earth_radius - y) / (earth_radius * 2 / tileNum))
    return [int(row),int(col)]
def rowcolToXYZ(row,col,zoom):
    tileNum = math.pow(2, zoom)
    x = (earth_radius * 2 / tileNum) * row - earth_radius
    y = earth_radius - (earth_radius * 2 / tileNum) * col
    return [x,y]

def drawMap(id,table,foldername,filename,city,county,branch,phone):
    sql = createSQL(table,city,county,branch)
    recordRows = []
    if table=='7':
        recordRows=getPGTableData(sql)
    else:
        recordRows = getTableData(sql.encode('utf-8'))
    maxextent = [180, 180,0, 0]
    for recordRow in recordRows:
        extent=extentByWKT(recordRow[3])
        if maxextent[0] > extent[0]:
            maxextent[0] = extent[0]
        if maxextent[1] > extent[1]:
            maxextent[1] = extent[1]
        if maxextent[2] < extent[2]:
            maxextent[2] = extent[2]
        if maxextent[3] < extent[3]:
            maxextent[3] = extent[3]
            
    _llcrnrlon=maxextent[0] -(maxextent[2]-maxextent[0])/10
    _llcrnrlat=maxextent[1] -(maxextent[3]-maxextent[1])/10
    _urcrnrlon=maxextent[2] +(maxextent[2]-maxextent[0])/10
    _urcrnrlat=maxextent[3] +(maxextent[3]-maxextent[1])/10
    minxy=millerToXY(_llcrnrlon,_llcrnrlat)
    maxxy=millerToXY(_urcrnrlon,_urcrnrlat)
    _width=abs(math.ceil((maxxy[0]-minxy[0])/10))
    _height=abs(math.ceil((maxxy[1]-minxy[1])/10))
    print(_width)
    print(_height)
    if _width>20000 or _height>20000:
        _width=_width/5
        _height=_height/5
    if _width>10000 or _height>10000:
        _width=_width/3
        _height=_height/3
    if _width>5000 or _height>5000:
        _width=_width/2
        _height=_height/2
        
    if _width<1000 or _height<1000:
        _width=_width*4
        _height=_height*4
    if _width<1500 or _height<1500:
        _width=_width*3
        _height=_height*3
    if _width<2000 or _height<2000:
        _width=_width*2
        _height=_height*2
    
    fig = plt.figure(figsize=(_width/96, _height/96),dpi=96) 
    ax = fig.add_axes([0, 0, 1, 1]) 
    map = Basemap(llcrnrlon=_llcrnrlon,llcrnrlat=_llcrnrlat,urcrnrlon=_urcrnrlon,urcrnrlat=_urcrnrlat,projection = 'merc', epsg=3857)
    map.arcgisimage(server='http://10.110.39.172:6080/arcgis',service='baselayer/SiChuan_All', xpixels =_width,ypixels =_height,verbose= True)
    for recordRow in recordRows:
        wkt=recordRow[3]
        extent=extentByWKT(wkt)
        patches=createPatches(map,wkt)
        _facecolor='#069F08'
        if recordRow[1]==1:
            _facecolor='#069F08'
        elif recordRow[1]==2:
            _facecolor='#0042AB'
        elif recordRow[1]==3:
            _facecolor='#B21702'
        patchcollection=PatchCollection(patches, facecolor=_facecolor, edgecolor='#FFFFFF', linewidths=1, zorder=2,alpha=0.5)
        ax.add_collection(patchcollection)
        if table=='7' or table=='8':
            _p=map((extent[0]+extent[2])/2,(extent[1]+extent[3])/2)
            plt.text(_p[0],_p[1], recordRow[2].decode("utf-8"),fontsize=10,color='#FFFFFF',ha='center')
    plt.axis('off')
    path=base_path+foldername
    newfile=path+'\\'+filename
    plt.savefig(newfile+'.png')
    #----------------------------------------------------------------------------------------------------------------------------------
    plt.clf()
    _fig = plt.figure(figsize=(_width/96, _height/96),dpi=96) 
    _ax = _fig.add_axes([0, 0, 1, 1]) 
    _map = Basemap(llcrnrlon=_llcrnrlon,llcrnrlat=_llcrnrlat,urcrnrlon=_urcrnrlon,urcrnrlat=_urcrnrlat,projection = 'merc', epsg=3857)
    _extent=[minxy[0],minxy[1],maxxy[0],maxxy[1]]
    zoom=calcLevel(_extent,_width,_height)
    top_left_row_col=xyzToRowCol(_extent[0],_extent[3],zoom)
    bottom_right_row_col=xyzToRowCol(_extent[2],_extent[1],zoom)
    resolution = (earth_radius * 2 / math.pow(2, zoom)) / 256
    min_point = rowcolToXYZ(top_left_row_col[0], bottom_right_row_col[1] + 1, zoom)

    max_point = [(min_point[0] + (bottom_right_row_col[0] - top_left_row_col[0] + 1) * resolution * 256), (min_point[1] + (bottom_right_row_col[1] - top_left_row_col[1] + 1) * resolution * 256)]
    
    image_width=int(bottom_right_row_col[0] - top_left_row_col[0] + 1) * 256
    image_height=int(bottom_right_row_col[1] - top_left_row_col[1] + 1) * 256
    
    targetImage=Image.new('RGBA',(image_width,image_height))
    for i in range(top_left_row_col[0],bottom_right_row_col[0]+1):
        for j in range(top_left_row_col[1],bottom_right_row_col[1]+1):
            tileCoord=[zoom,i,j]
            oo='00000000'
            zz=tileCoord[0]
            if zz<10:
                zz='0'+str(zz)
            z='L'+str(zz)
            xx=hex(tileCoord[1]).replace('0x','')
            x='C'+oo[0:(8-len(xx))]+xx
            yy=hex(tileCoord[2]).replace('0x','')
            y='R'+oo[0:(8-len(yy))]+yy
            im=Image.open('\\\\WYZX-DESKTOP-00\\ImageLayer\\Layers\\_alllayers\\'+z+'\\'+y+'\\'+x+'.png')
            targetImage.paste(im, ((i-top_left_row_col[0])*256,(j-top_left_row_col[1])*256))
    
    left=(_extent[0]-min_point[0])/resolution
    upper=(max_point[1]-_extent[3])/resolution
    left=(_extent[0]-min_point[0])/resolution
    upper=(max_point[1]-_extent[3])/resolution
    right=image_width-(max_point[0]-_extent[2])/resolution
    lower=image_height-(_extent[1]-min_point[1])/resolution
    resultImage=targetImage.crop((left,upper,right,lower)).resize((int(_width),int(_height)))
    x0, y0 = _map(_llcrnrlon, _llcrnrlat)
    x1, y1 = _map(_urcrnrlon, _urcrnrlat)
    plt.imshow(resultImage,  extent = (x0, x1, y0, y1))
    for recordRow in recordRows:
        wkt=recordRow[3]
        extent=extentByWKT(wkt)
        patches=createPatches(_map,wkt)
        _facecolor='#069F08'
        if recordRow[1]==1:
            _facecolor='#069F08'
        elif recordRow[1]==2:
            _facecolor='#0042AB'
        elif recordRow[1]==3:
            _facecolor='#B21702'
        patchcollection=PatchCollection(patches, facecolor=_facecolor, edgecolor='#FFFFFF', linewidths=1, zorder=2,alpha=0.5)
        _ax.add_collection(patchcollection)
        if table=='7' or table=='8':
            _p=_map((extent[0]+extent[2])/2,(extent[1]+extent[3])/2)
            plt.text(_p[0],_p[1], recordRow[2].decode("utf-8"),fontsize=10,color='#FFFFFF',ha='center')
    plt.axis('off')
    plt.savefig(newfile+'_image.png')
    #----------------------------------------------------------------------------------------------------------------------------------
    zipDir(path,base_path+foldername+'.zip','')
    updateStatusAndURL(id,download_path+foldername+'.zip')
    inertInfo(phone,filename+'已经导出完成！')
    logging.info(filename+u'导出完成')
    gc.collect()
    exit()
        
def writeToTAB(id,table,city,county,branch,phone):
    tablelabel=''
    if table=='1':
        tablelabel=u'物业点'
    if table=='2':
        tablelabel=u'楼宇'
    if table=='3':
        tablelabel=u'自然村'
    if table=='4':
        tablelabel=u'网格'
    if table=='5':
        tablelabel=u'口碑场景'
    if table=='6':
        tablelabel=u'集团客户'
    if table=='7':
        tablelabel=u'自然村渲染图'
    if table=='8':
        tablelabel=u'物业点渲染图'
    if table=='9':
        tablelabel=u'楼宇渲染图'
        
    foldername=phone+'_'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'_'+tablelabel
    path=base_path+foldername
    if os.path.isdir(path)==False:
        os.mkdir(path)
    
    filename=tablelabel
    if city!='' and city !=None:
        filename+='_'+city
    if county!='' and county !=None:
        filename+='_'+county
    if branch!='' and branch !=None:
        filename+='_'+branch
    
    newfile=path+'\\'+filename
    if table=='7':
        drawMap(id,table,foldername,filename,city,county,branch,phone)
        return
    if table=='8':
        drawMap(id,table,foldername,filename,city,county,branch,phone)
        return
    if table=='9':
        drawMap(id,table,foldername,filename,city,county,branch,phone)
        return
    
    if os.path.exists(newfile+'.TAB')==False:
        shutil.copyfile(template_path+tablelabel+'.TAB',newfile+'.TAB')
        shutil.copyfile(template_path+tablelabel+'.DAT',newfile+'.DAT')
        shutil.copyfile(template_path+tablelabel+'.MAP',newfile+'.MAP')
        shutil.copyfile(template_path+tablelabel+'.ID',newfile+'.ID')
        
    time.sleep(1)
    ds = ogr.Open(newfile+'.TAB',True) #False - read only, True - read/write
    oLayer = ds.GetLayer(0)
    oDefn = oLayer.GetLayerDefn()  # 定义要素
    
    #ogr.RegisterAll()  # 注册所有的驱动
    #gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
    #gdal.SetConfigOption("SHAPE_ENCODING", "")
    

    sql = createSQL(table,city,county,branch)
    recordRows = getTableData(sql)
    for recordRow in recordRows:
        feature = ogr.Feature(oDefn)
        fields=getFields(table)
        for i in range(len(fields)):
            if fields[i]['field_type']=='s':
                if recordRow[i]!='' and recordRow[i]!=None:
                    feature.SetField(i, str(recordRow[i]).encode('gbk'))
                else:
                    feature.SetField(i, recordRow[i])
            elif fields[i]['field_type']=='f':
                if recordRow[i]!=None:
                    feature.SetField(i, float(recordRow[i]))
                else:
                    feature.SetField(i, recordRow[i])
            else:
                if recordRow[i]!=None:
                    feature.SetField(i, int(recordRow[i]))
                else:
                    feature.SetField(i, recordRow[i])
        if recordRow[len(fields)]==None:
			continue
        geom =ogr.CreateGeometryFromWkt(recordRow[len(fields)])
        feature.SetGeometry(geom)
        oLayer.CreateFeature(feature)
    ds.Destroy()
    ds=None
    oLayer=None
    oDefn=None
    zipDir(path,base_path+foldername+'.zip','')
    updateStatusAndURL(id,download_path+foldername+'.zip')
    inertInfo(phone,filename+'已经导出完成！')
    logging.info(filename+u'导出完成')
    gc.collect()
    exit()
    
if __name__ == '__main__':
    getUnResolving()