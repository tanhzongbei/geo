#coding:utf8
'''
Created on 2013-8-5

@author: xiaobei
'''
from kapi.logger import TCPLogger
import config as _cnf
import logging

#------------------------------------------------------------------------------ 

logger = TCPLogger(*_cnf.LOG_ADDR, size=_cnf.LOG_BUFFER, flush_level=logging.ERROR)


def recordErr(funcname, args, errcode):
    args_msg = '' 
    if isinstance(args, tuple):
        for i in xrange(len(args)):
            args_msg.append('%s' % str(args[i]))
    err_msg = 'function is %s, params is %s, err code is %s' % (funcname, args_msg, errcode)
    logger.error(err_msg) 


def main():
    pass
    
if __name__ == "__main__":
    main()