#coding:utf8
'''
Created on Feb 26, 2014

@author: ilcwd
'''
import os
import urllib2
import urllib
import json
import Image
from ExifTags import TAGS
from collections import defaultdict

import geohash
import memcache

mc = memcache.Client(['10.0.3.184'])

def cacheit(func):
    def _w(latitude, longitude):
        key = str(latitude) + "," + str(longitude)
        addr = mc.get(key)
        if addr is None:
            addr = func(latitude, longitude)
            mc.set(key, addr)
            
        return addr
    return _w

@cacheit
def gps_to_address(latitude, longitude):
    base = 'http://api.map.baidu.com/geocoder/v2/'
    params = dict(
        ak = 'QQYyfndLXSRzUskAq69lZuk4',
        location = str(latitude) + "," + str(longitude),
        output = 'json',
        pois = 0,
        coordtype = 'wgs84ll',
    )
    url = base + '?' + urllib.urlencode(params)
    result = urllib2.urlopen(url).read()
    return json.loads(result)


def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    img = Image.open(fname)
    if hasattr(img, '_getexif' ):
        exifinfo = img._getexif()
        if exifinfo != None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    return ret


def from_degrees(info):
    (d, dp), (m, mp), (s, sp) = info
    return float(d)/dp + float(m)/mp/60 + float(s)/sp/3600


def get_gps_info(fname):
    img = Image.open(fname)
    if hasattr(img, '_getexif' ):
        exifinfo = img._getexif()
        if exifinfo != None:
            gpsinfo = exifinfo.get(0x8825) # 0x8825 = GPSInfo
            if not gpsinfo: return
            
            GPSLatitudeRef = gpsinfo[1]
            GPSLatitude = gpsinfo[2]
            GPSLongitudeRef = gpsinfo[3]
            GPSLongitude = gpsinfo[4]
            
            latitude = from_degrees(GPSLatitude)
            longitude = from_degrees(GPSLongitude)
            return (latitude, longitude)
    return None



def catalog_by_city(dir):
    result = defaultdict(list)
    
    def _get_city_from_addr(addr):
        return addr['result']['addressComponent']['province'] + addr['result']['addressComponent']['city']
    
    for f in os.listdir(dir):
        fpath = os.path.join(dir, f)
        
        gpsinfo = get_gps_info(fpath)
        if not gpsinfo:
            result[u'未知地区'].append(f)
            continue
            
        addr = gps_to_address(*gpsinfo)
        city = _get_city_from_addr(addr)
        
        result[city].append(f)
        
    for k, v in result.iteritems():
        print k
        print '\t', ','.join(v)
        

def main():
#     print geohash.bbox('u4pruydqqvj')
#     print geohash.neighbors('u4pruydqqvj')
#     
#     fpath = '/home/ilcwd/Pictures/photos/IMG_0498_x.jpg'
#     gpsinfo = get_gps_info(fpath)
#     print gps_to_address(*gpsinfo)['result']
    
    catalog_by_city('/home/twotrees/pictrue')

if __name__ == '__main__':
    main()