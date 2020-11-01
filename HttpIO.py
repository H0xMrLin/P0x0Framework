#coding:utf-8
import time;
#from cgi import parse_qs;
import urllib;
import cgi
import cgitb; cgitb.enable()
class HttpResponse:
    def __init__(self,Context,ContentType="text/html"):
        self.Status=200;
        if( type(Context) !=bytes):
            self.ResponseContext=bytes(Context,encoding='UTF-8');
        else:
            self.ResponseContext=Context;
        self.SetCookies=None;
        self.Headers={};
        self.Cookies={};
        self.ContentType=ContentType
    def SetCookie(self,key,value,dt=time.time()+15552000):
        dtc=time.localtime(dt)
        datetimestr=time.strftime('%a, %d %b %Y %H:%M:%S GMT',dtc)
        self.Cookies[key]=value+";expires="+datetimestr;
    def Reinner(self,Context):
        if( type(Context) !=bytes):
            self.ResponseContext=bytes(Context,encoding='UTF-8');
        else:
            self.ResponseContext=Context;
class HttpRequest:
    def init_Session(self):
        print("[Session]:");
    def __init__(self,environ):
        self.environ=environ;
        self.Remote_Addr=environ['REMOTE_ADDR'];
        self.Path=environ['PATH_INFO'];
        self.StaticFile=self.Path.lower()[:7]=="/static";
        self.ReuqestMethod=environ['REQUEST_METHOD'];
        self.Cookies={};
        #处理POST数组
        #try:
        #    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        #except (ValueError):
        #    request_body_size = 0
        #request_body = environ['wsgi.input'].read(request_body_size)
        #tmpPOST=urllib.parse.parse_qs((request_body.decode('utf-8'))) # parse_qs(request_body)
        self.POST={};
        self.FILE={};
        #for Key,Value in tmpPOST.items():
        #    self.POST[Key]=Value;
        #print(str(self.POST));
        #if(environ['CONTENT_TYPE']=='multipart')
        #for Postkey,PostValue in tmpPOST.items():
        #    self.POST[Postkey.strip()]=PostValue[0];
        #if 'POST' == environ['REQUEST_METHOD'] and (environ['CONTENT_TYPE'][:9]=='multipart'):
        if 'POST' == environ['REQUEST_METHOD']:
            fields = cgi.FieldStorage(fp=environ['wsgi.input'],environ=environ, keep_blank_values=1);
            for item in fields.keys():
                #if(None == None):
                #    self.POST[item]=fields[item].value;
                #else:
                #    self.POST[item]=fields[item].filename;
                try:
                    if(getattr(fields[item],'filename') != None):
                        self.POST[fields[item].name]=fields[item].filename;
                        self.FILE[fields[item].filename]=fields[item].value;
                        continue;
                except:
                    None;
                self.POST[fields[item].name]=fields[item].value;

            #self.POST=(fields.keys());
        #处理GET数据数组
        if('QUERY_STRING' in environ.keys()):
            self.GET=urllib.parse.parse_qs(environ['QUERY_STRING'])
            for Getkey,GetValue in self.GET.items():
                self.GET[Getkey]=GetValue[0];
        else:
            self.GET=[];
        try:
            CookieSource=environ['HTTP_COOKIE'];
            CookieLines=CookieSource.split(";");
            for Cookie in CookieLines:
                c=Cookie.split("=");
                key,value=c[0],c[1];
                self.Cookies[key.strip()]=value;
        except:
            None;
        for key,value in environ.items():
            setattr(self,key,value);
        """
        try:
            self.HTTP_HOST=environ['HTTP_HOST'];
            self.HTTP_USER_AGENT=environ['HTTP_USER_AGENT'];
            self.HTTP_ACCEPT=environ['HTTP_ACCEPT'];
            self.HTTP_ACCEPT_LANGUAGE=environ['HTTP_ACCEPT_LANGUAGE'];
            self.HTTP_ACCEPT_ENCODING=environ['HTTP_ACCEPT_ENCODING'];
            self.HTTP_CONNECTION=environ['HTTP_CONNECTION'];
            self.HTTP_UPGRADE_INSECURE_REQUESTS=environ['HTTP_UPGRADE_INSECURE_REQUESTS'];
            self.HTTP_PRAGMA=environ['HTTP_PRAGMA'];
            self.HTTP_CACHE_CONTROL=environ['HTTP_CACHE_CONTROL'];
        except:
            None;"""
        
