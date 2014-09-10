#coding:utf8
'''
Created on 2014-2-21

@author: xiaobei
'''

import sys
reload(sys).setdefaultencoding('utf8')
sys.path.append('/data/apps/apipublic')

from kapi.server import jsonserver2
from logger import logger

server = jsonserver2.JSONWSGIServer()
server.set_logger(logger)
server.load_module('location')

application = server.get_wsgi_application()


def debug_main():
    import web
    web.debug = True
    bind_addr = ('0.0.0.0', 9203)
    print "INFO: Server Start on %s" % str(bind_addr)
    web.httpserver.runsimple(application, bind_addr)


if __name__ == '__main__':
    debug_main()