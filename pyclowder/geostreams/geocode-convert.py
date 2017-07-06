from LatLon import LatLon
from LatLon import Latitude
from LatLon import Longitude

def dms2dec(dms):
    # dms = [[44,17,28.7],[94,4,32.5]]

    dec = LatLon(Latitude(degree = dms[0][0], minute = dms[0][1], second = dms[0][2]), Longitude(degree = dms[1][0], minute = dms[1][1], second = dms[1][2]))

    return dec