#encoding:utf-8
from wsgiref.simple_server import make_server
import sys;
import importlib;
import imp;
#并发占用资源生产环境下使用
#import socket;
#socket.setdefaulttimeout(30);
try:
    PORT=int(sys.argv[1]);
except:
    PORT= 8080;
def Main(environ,statrt_response):
    #statrt_response('200 OK',[('Content-Type', 'text/html')])
    #return [b'<h1>404 Files notExists</h1>']
    driver=imp.reload( importlib.import_module('driver'));
    return driver.driver_init(environ,statrt_response);
if(__name__ == '__main__'):
    print("[+]Loading HttpServer");
    httpd =make_server('',PORT,Main);
    print("[+]Start Service···")
    httpd.serve_forever();
