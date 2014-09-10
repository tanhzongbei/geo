#coding:utf8
'''
Created on 2014-2-21

@author: xiaobei
'''
import sys
sys.path.append('../../')

from module.persistconn import connTest as conn
from kapi import  mysqltools2 as _sqltool
import getdistance 
import math

#===============================================================================
#纬度1'' = 30.8m，经度 1'' = 30.8  
#distance 单位是km
#===============================================================================
def getPointsByCenterGPS(point, distance):
    lng, lat = point
    lngdegree = math.acos(float(distance) / float(30.8 * 3.6))
    latdegree = float(distance) / float(30.8 * 3.6 )
    l1 = (lng - lngdegree, lat - latdegree)
    l2 = (lng + lngdegree, lat - latdegree)
    l3 = (lng + lngdegree, lat + latdegree)
    l4 = (lng - lngdegree, lat + latdegree)
    
    return l1, l2, l3, l4
#===============================================================================
#按逆时针方向
#
#l4-----l3
#|       |
#|       |
#l1-----l2
#===============================================================================
def queryOthersByGPS(point, distance):
    l1, l2, l3, l4 = getPointsByCenterGPS(point, distance)
    try:         
        SQL = ('''SELECT `id`, AsText(gps) FROM `geotest` WHERE MBRContains(GeomFromText('Polygon((%.10f %.10f,%.10f %.10f,%.10f %.10f,%.10f %.10f, %.10f %.10f))'), `gps`);
                '''
                % (l1[0], l1[1], l2[0], l2[1], l3[0], l3[1], l4[0], l4[1], l1[0], l1[1]))
        res = conn.query(SQL)
        return res
    except _sqltool.SQLOperationalError as e:
        return None
        
    
def insertPoint(point):
    try:
        SQL = '''SET @g = GeomFromText('Point(%.10f %.10f)');
                 INSERT INTO `geotest` (`gps`) VALUES (@g);
        ''' % (point[0], point[1])
        res = conn.execute(SQL)
        return res
    except _sqltool.SQLOperationalError as e:
        return None


if __name__ == '__main__':
    xizhan = {}
    xizhan['lat'] = (39.9005979673, 'N')
    xizhan['lng'] = (116.3275833876, 'E')
    
    kingsoft = {}
    kingsoft['lat'] = (40.0430568762, 'N')
    kingsoft['lng'] = (116.3299773912, 'E')
    
    tiyudaxue = {}
    tiyudaxue['lat'] = (40.0298761189, 'N')
    tiyudaxue['lng'] = (116.3244213149, 'E')
    
    kanpeila = {}
    kanpeila['lat'] = (-35.2819998000, 'S')
    kanpeila['lng'] = (149.1286843000, 'E')
    
    art798 = {}
    art798['lng'] = (116.5019368136, 'E')
    art798['lat'] = (39.9906971738, 'N')
    
    
    print getdistance.getDistance(kingsoft, xizhan)
    print getdistance.getDistance(kingsoft, tiyudaxue)  
#    print getdistance.getDistance(kingsoft, kanpeila)  
    print getdistance.getDistance(kingsoft, art798)  
    
#    insertPoint((xizhan['lng'][0], xizhan['lat'][0]))
#    insertPoint((kingsoft['lng'][0], kingsoft['lat'][0]))
#    insertPoint((kanpeila['lng'][0], kanpeila['lat'][0]))       
#    insertPoint((tiyudaxue['lng'][0], tiyudaxue['lat'][0]))        
#    insertPoint((art798['lng'][0], art798['lat'][0]))        

    print queryOthersByGPS((kingsoft['lng'][0], kingsoft['lat'][0]), 6)

    