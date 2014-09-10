#coding:utf8
'''
Created on 2014-2-19

@author: xiaobei
'''
import sys
sys.path.append('../../')

import math
import ujson as _json
from kapi.urltools import curl
import config as _cnf

#------------------------------------------------------------------------------ 

EARTH_RADIUS = 6378.137


def rad(d):
    return d * math.pi / 180.0


def getDistance(point1, point2):
    lat1 = dealLat(point1['lat'][0], point1['lat'][1]) 
    lng1 = dealLng(point1['lng'][0], point1['lng'][1]) 
    lat2 = dealLat(point2['lat'][0], point2['lat'][1]) 
    lng2 = dealLng(point2['lng'][0], point2['lng'][1])
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s = s * EARTH_RADIUS
    s = round(s * 10000) / 10000
    return s

#===============================================================================
# 设第一点A的经纬度为(LonA, LatA)，第二点B的经纬度为(LonB, LatB)，
# 按照0度经线的基准，东经取经度的正值(Longitude)，西经取经度负值(-Longitude)，
# 北纬取90-纬度值(90-Latitude)，南纬取90+纬度值(90+Latitude)，
#===============================================================================
def dealLat(lat, ref):
    if ref == 'N':
        return 90 - abs(lat)
    else:
        return 90 + abs(lat)

def dealLng(lng, ref):
    if ref == 'E':
        return abs(lng)
    else:
        return 0 - abs(lng)
            

def getLocation(lng, lat):
    url = _cnf.BAIDU_URL + 'ak=%s&' % _cnf.BAIDU_AK + 'location=%s,%s&output=json&pois=0' % (str(lat),str(lng))
    code, res = curl.openurl(url)
    result = {}
    res = _json.loads(res)
    if code == 200 and res['status'] == 0:
        result = res['result']
        return result
    else:
        return 'error'
    

if __name__ == '__main__':
    print getLocation(37.3625170000, -122.0347600000)
    
    
    
    