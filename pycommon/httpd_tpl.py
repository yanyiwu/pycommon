#!/usr/bin/python
#coding:utf8

import sys,os

import urlparse
import BaseHTTPServer
from pylogger import logger
import utilities as functs

class HTTPReqHandlerTpl(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def do_GET(self):
        ret_html = '<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body>hello_world</body></html>' 
        self.wfile.write(ret_html)
        pass

    def do_POST(self):
        pass

if __name__ == "__main__":
    port = 11256
    httpd = BaseHTTPServer.HTTPServer(("", port), HTTPReqHandlerTpl)
    httpd.serve_forever()
