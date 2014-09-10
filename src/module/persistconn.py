#coding:utf8
'''
Created on 2012-9-14

@author: ilcwd
'''
import sys
sys.path.append('../../')

from kapi.mysqltools import (
    MySQLConnManager,
    MysqlExecutor
)
from kapi import misc as _misc
import config as _conf

connTest = MysqlExecutor(MySQLConnManager(**_conf.MYSQL_GEOTEST))

START_TIME = _misc.now()

def main():
    SQL = 'select * from `geotest`;'
    print connTest.query(SQL)    
    
if __name__ == "__main__":
    main()