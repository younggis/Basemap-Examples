lon = 104
lat = 30

axesm()

geoshow('cn_province',edgecolor='k')

layer = scatterm(lon,lat,size=40,marker='image',imagepath=r'H:\Python\Basemap-Examples\images\loc.png')

xlim(70,140)
ylim(10,60)