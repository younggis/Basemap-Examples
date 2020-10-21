# -*- coding: utf-8 -*-
# @Author: wuzida
# @Date:   2018-12-28 15:20:54
# @Last Modified by:   wuzida
# @Last Modified time: 2018-12-29 16:49:14



import geo
import scipy.io as sio
from numpy import*


print geo.geodetic_to_ecef(30,104,0)
print geo.ecef_to_geodetic(-1337406.,5364044.,3170374.)

print geo.enu_to_geodetic(612.3724356957945,612.3724356957946,499.99999999999994,30,104,0)

#print geo.enu_to_geodetic(346.41,-600,400,30,104,0)