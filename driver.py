#encoding:utf-8
#import HttpIO;
import router;
import importlib;
import imp;
import re;
import os;
import uuid;
import Sessionbase;
HttpIO=imp.reload( importlib.import_module('HttpIO'));
urls=imp.reload( importlib.import_module('urls'));
#Sessionbase=imp.reload( importlib.import_module('Sessionbase'));
#check must cookie
def rdb_Check(hq,hp):
    Must_CookieKey=['fmsid','sessionid','postid']
    ExistsMustCookieKey=True;
    for key in Must_CookieKey:
        if not( key in hq.Cookies.keys()):
            hp.SetCookie(key,str(uuid.uuid4()));
            ExistsMustCookieKey=ExistsMustCookieKey&False;
        else:
            ExistsMustCookieKey=ExistsMustCookieKey&True;
    return ExistsMustCookieKey;
#static File:
def staticFile(hq):
    File=hq.Path;
    mimeJsonp=open("mime.json");
    mimeJson=eval(mimeJsonp.read());
    #ReFileName=re.findall("/static/(([A-Z]|[a-z]|[0-9]|/|\.)+(([A-Z]|[a-z]|[0-9])+))",hq.Path)[0];
    #ReFileName=re.findall("/static/(.+)",hq.Path)[0];
    FileName=hq.Path[1:];
    FileName=FileName.replace("..","");
    #FileName=ReFileName[0];
    LastFileName="."+FileName.split(".")[-1];
    ContentType="text/html";
    if(LastFileName in mimeJson.keys()):
        ContentType=mimeJson[LastFileName];
    #print(""+FileName);
    if not(os.path.exists(""+FileName.strip())):
        ContentType="text/html";
        FileBytes="404 File not exists";
    else:
        fileOpen=open(""+FileName,"rb");
        FileBytes=fileOpen.read();
    if( type(FileBytes) == str):
        FileBytes=bytes(FileBytes,encoding='UTF-8');
    return ContentType,FileBytes
def driver_init(environ,statrt_response):
    HttpRequest=HttpIO.HttpRequest(environ);
    if(HttpRequest.StaticFile):
        mime,data=staticFile(HttpRequest);
        statrt_response('200 OK',[("content-Type",mime)]);
        #print(mime,data);
        return [data];
    if( "fmsid" in HttpRequest.Cookies.keys()):
        SessionID=HttpRequest.Cookies["fmsid"];
        try:
            tSession=eval(Sessionbase.GetSession(SessionID));
        except:
            tSession={};
    else:
        tSession={};
    eqSession=str(tSession);
    if( HttpRequest.Path in urls.urls):
        HttpResponse=urls.urls[HttpRequest.Path](HttpRequest,tSession)
        resHeaders=[('Content-Type', HttpResponse.ContentType),('Server','Baotav3.7')];
        #Check mustcookie and update session
        if not(rdb_Check(HttpRequest,HttpResponse)):
            #print(str(HttpResponse.Cookies))
            try:
                SessionID=HttpResponse.Cookies["fmsid"];
            except:
                SessionID=HttpRequest.Cookies["fmsid"];
            Sessionbase.WriteSession(SessionID,str(tSession));
        else:
            if (eqSession!=str(tSession)):
                SessionID=HttpRequest.Cookies["fmsid"];
                Sessionbase.UpdateSession(SessionID,str(tSession));
        #Set-Cookie:
        for Cookie in HttpResponse.Cookies.keys():
            resHeaders.append( ('set-cookie',Cookie+"="+HttpResponse.Cookies[Cookie]) )
        #Response header
        for headerName in HttpResponse.Headers.keys():
            resHeaders.append( (headerName,HttpResponse.Headers[headerName]))
        statrt_response(str(HttpResponse.Status)+' OK',resHeaders)
        return [HttpResponse.ResponseContext];
    statrt_response('404 OK',[('Content-Type', 'text/html'),('Server','Apache2'),('Set-Cookie','failed=404; expires=Fri, 17 Jun 2090 16:06:06 GMT;')])
    return [b"404 Files not exists"]