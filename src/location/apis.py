#coding:utf8
'''
Created on 2014-2-21

@author: xiaobei
'''
import module.getdistance as _dis

#------------------------------------------------------------------------------ 


def test(request):
    pass


def registGPS(request, lat, lng):
    pass


def queryLocationByGPS(request, lng, lat):
    #公共服务，GPS坐标不一定在数据库中
    res = _dis.getLocation(lng, lat)
    return res


def queryLocationAround(request, lat, lng):
    pass

#------------------------------------------------------------------------------ 

def main():
    pass


if __name__ == '__main__':
    main()