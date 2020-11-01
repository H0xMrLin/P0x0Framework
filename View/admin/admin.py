# coding=utf-8
import HttpIO;
import router;
import os;
#from Dal import aos;
#from Lib import Template;
import importlib;
import imp;
import json;
import time;
import sqlite3;
import re;
import uuid;
import urllib;
import copy;
import base64;
aos=imp.reload( importlib.import_module("Dal.aos"));
Template=imp.reload( importlib.import_module("Lib.Template"));
baseUrl=aos.SystemSetting.Select(Key="BaseUrl")[0].Value;
def LogOp(Opname,OpContext,ip,Username):
    OpradeLog=aos.adminOpradeLog();
    OpradeLog.ip=ip;
    OpradeLog.OpradeUsername=Username;
    OpradeLog.OpradeDateTime=time.time();
    OpradeLog.OpradeContent= urllib.parse.quote(str([Opname,OpContext]));#urllib.parse.urlencode(str({'ActionFunc':Opname,'ActionParamter':str(OpContext)}));
    aos.adminOpradeLog.Insert([OpradeLog]);

def PPLog(HttpRequest,Session,Username,Action):
    LogOp(Action,{"GET":str(HttpRequest.GET),"POST":str(HttpRequest.POST),"Session":str(Session)}, HttpRequest.Remote_Addr,Username);

def CheckAuth(Username,Auth,ip):
    if(Username.strip()=='' or Auth.strip()==''):
        return False;
    CurAuth=aos.adminAuth.Select(AuthKey=Auth,Username=Username)[-1];
    if(CurAuth.ip != ip):
        return False;
    return True;
def CreateAuth(Username,Password,ip):
    Count=aos.adminUserInfo.Select(Username=Username,Password=Password,DataMethod={'Enable':True,'Method':'Count','FiledName':"ID"});
    if(Count != 1):
        return None;
    AuthCode=str(uuid.uuid1()).replace('-','');
    AuthObj=aos.adminAuth();
    AuthObj.AuthKey=AuthCode;
    AuthObj.Username=Username;
    AuthObj.AuthDateTime=str(time.time());
    AuthObj.ip=ip
    Success=aos.adminAuth.Insert([AuthObj]);
    if(Success):
        return AuthCode;
    else:
        return None;
@router.Router("/"+baseUrl,True)
def index(HttpRequest,Session):
    htr=HttpIO.HttpResponse("""
    <meta http-equiv="content-type" content="text/html;charset=utf-8"><center>
    <h1>Wecome to 0x0Frame Admin!</h1>
    <img src="/static/timg.jpg" /><br/>
    <form action="{{action}}" method="POST"><table><tr><th>Username:<input type='text' name='username' /></tr></tr><tr><th>Password:<input name='password' type="password" /></th></tr><tr><th><input type="submit" value="登录" /></th></tr></table>
    </center>
    <style>
    body{
        background-color:#20252e;
        color:#FFFFFF;
    }
    img{
        /*widtr:100%;*/
    }
    h1{
        color:#FFFFFF;
        font-size: 500%;
    }
    </style>
    """.replace("{{action}}","/"+baseUrl+"/adminmeLogin"));
    return htr;
@router.Router("/"+baseUrl+"/adminmeLogin",True)
def adminmeLogin(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        try:
            Username=HttpRequest.POST["username"].strip();
            Password=HttpRequest.POST["password"].strip();
        except:
            return HttpIO.HttpResponse("Exm?");
        AuthCode=CreateAuth(Username,Password,HttpRequest.Remote_Addr);
        if(AuthCode == None):
            return HttpIO.HttpResponse("Login failed!");
        Session["AuthCode"]=AuthCode;
        Session["Username"]=Username;
        LogOp("登入账号",{"GET":str(HttpRequest.GET),"POST":str(HttpRequest.POST),"Session":str(Session)}, HttpRequest.Remote_Addr,Username)
    UserInfo=aos.adminUserInfo.Select(Username=Username);
    return Template.View("admin/adminIndex.shtml",{"UserInfo":(UserInfo),"outLoginHref":"/"+baseUrl+"/OutLogin"});
@router.Router("/"+baseUrl+"/index_init.json",True)
def init_Json(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    dbNames=os.listdir(os.getcwd()+"/sqliteDB/");
    ShowList=[]
    
    for dbName in dbNames:
        tables=[]
        dbLib = imp.reload( importlib.import_module("Dal."+dbName[:-3]));
        ChildTmplt={"title": "数据库:"+dbName,"icon": "fa fa-database","href": "","target": "_self","child":tables};
        for tbName in dbLib.tables:
            tables.append({"title": ""+tbName,"icon": "fa fa-table","href": "/"+baseUrl+"/sqlOP?db="+dbName+"&tb="+tbName,"target": "_self"});
        ShowList.append(ChildTmplt);
    HttpResponse=Template.View("admin/init.json",{"DBShowList":str(ShowList)});
    HttpResponse.ContentType="application/x-javascript";
    return HttpResponse;
@router.Router("/"+baseUrl+"/SystemSetting",True)
def SystemSeting(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    return;
@router.Router("/"+baseUrl+"/OutLogin",True)
def OutLogin(HttpRequest,Session):
    PPLog(HttpRequest,Session,Session['Username'],"退出账号")
    #Session['AuthCode']='ktCat';
    #Session['Username']='wdnmdUsername';
    Session.clear();
    return HttpIO.HttpResponse("<script>alert('Out Loing Success,Last 2s Goto FirstPage');setInterval(function(){document.location.href='/"+baseUrl+"'},2000)</script>");
@router.Router("/"+baseUrl+"/sqlOP")
def adminsqlOP(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    dbName=HttpRequest.GET["db"];
    tbName=HttpRequest.GET["tb"];
    #PageIndex=HttpRequest.GET["PageIndex"];
    dbName=dbName[:-3];
    dbLib = imp.reload( importlib.import_module("Dal."+dbName));
    tbLib=eval("dbLib."+tbName);
    PPLog(HttpRequest,Session,Session['Username'],"访问数据: 数据库："+dbName+" 表："+tbName)
    rowDefine=[];
    #print(tbLib.TableFileds);
    rowDefine.append( {"type": "checkbox", "width": 50});
    for TbFdName in tbLib.TableFileds:
        tmpT={"field": TbFdName, "title": TbFdName, "sort": "true"}
        rowDefine.append(tmpT);
    
    return Template.View("admin/admindb.shtml",{'databaseName':dbName,"TbFdName":str(rowDefine),"json":"/"+baseUrl+"/table.json?db="+dbName+"&tb="+tbName});
@router.Router("/"+baseUrl+"/table.json")
def adminsqlTable(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    dbName=HttpRequest.GET["db"];
    tbName=HttpRequest.GET["tb"];
    page=HttpRequest.GET["page"];
    limit=HttpRequest.GET["limit"];
    page=int(page)-1;
    limit=int(limit);
    dbLib = imp.reload( importlib.import_module("Dal."+dbName));
    tbLib=eval("dbLib."+tbName);
    data=[];
    Count=tbLib.Select(DataMethod={'Enable':True,'FiledName':tbLib.TableFileds[0],'Method':'Count' });
    for rowData in tbLib.Select(Limit={'Enable':True,'orderby':tbLib.TableFileds[0],'index':page*limit,'length':limit,'desc':False}):
        tmpDic={};
        for Filed in tbLib.TableFileds:
            tmpDic[Filed]=getattr(rowData,Filed);
        data.append(tmpDic);
    
    HttpResponse=Template.View("admin/table.json",{'data':json.dumps(data),'Count':Count});
    HttpResponse.ContentType="application/x-javascript";
    return HttpResponse;

@router.Router("/"+baseUrl+"/svrSetting")
def svrSetting(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    if(HttpRequest.ReuqestMethod=="POST"):
        for key,value in HttpRequest.POST.items():
            aos.SystemSetting.Select(Key=key)[0].Update(Value=value);
        PPLog(HttpRequest,Session,Username,"修改服务器配置");
        return HttpIO.HttpResponse("<h1>保存完成</h1><script>setTimeout(function(){document.location.href='svrSetting'},2000);</script>"+str(HttpRequest.POST));
    SystemSetting=aos.SystemSetting.Select();
    ss={};
    for ob in SystemSetting:
        ss[ob.Key]=ob.Value;
    return Template.View("admin/svrSetting.shtml",{"Ss":json.dumps(ss)});

@router.Router("/"+baseUrl+"/Loglist")
def Loglist(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    LogOp("查看日志",{"GET":str(HttpRequest.GET),"POST":str(HttpRequest.POST),"Session":str(Session)}, HttpRequest.Remote_Addr,Username)
    return Template.View("admin/admindb.shtml",{"json":"/"+baseUrl+"/LoglistJson","TbFdName":json.dumps([
                                                                                                        {"field": "SessionPar", "title": "Session参数", "sort": "true"},
                                                                                                        {"field": "POSTPar", "title": "POST参数", "sort": "true"},
                                                                                                        {"field": "GETPar", "title": "GET参数", "sort": "true"},
                                                                                                        {"field": "OpradeUsername", "title": "操作用户", "sort": "true"},
                                                                                                        {"field": "OpradeContent", "title": "操作内容", "sort": "true"},
                                                                                                        {"field": "OpradeDateTime", "title": "操作时间", "sort": "true"}
                                                                                                        ])})

@router.Router("/"+baseUrl+"/LoglistJson")
def LoglistJson(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    page=HttpRequest.GET["page"];
    limit=HttpRequest.GET["limit"];
    page=int(page)-1;
    limit=int(limit);
    data=[];
    Count=aos.adminOpradeLog.Select(DataMethod={'Enable':True,'FiledName':aos.adminOpradeLog.TableFileds[0],'Method':'Count' });
    for rowData in aos.adminOpradeLog.Select(Limit={'Enable':True,'orderby':aos.adminOpradeLog.TableFileds[0],'index':page*limit,'length':limit,'desc':True}):
        tmpDic={};
        #for Filed in aos.adminOpradeLog.TableFileds:
        #    tmpDic[Filed]=getattr(rowData,Filed);
        OpradeContent=eval(urllib.parse.unquote(rowData.OpradeContent));
        tmpDic["OpradeContent"]=OpradeContent[0];
        tmpDic["SessionPar"]=str(OpradeContent[1]["Session"]);
        tmpDic["GETPar"]=str(OpradeContent[1]["GET"]);
        tmpDic["POSTPar"]=str(OpradeContent[1]["POST"]);
        tmpDic["OpradeUsername"]=rowData.OpradeUsername;
        tmpDic["OpradeDateTime"]= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( rowData.OpradeDateTime));
        data.append(tmpDic);
    HttpResponse=Template.View("admin/table.json",{'data':json.dumps(data),'Count':Count});
    HttpResponse.ContentType="application/x-javascript";
    return HttpResponse;
def travelTree(currentPath, count=0):
    if not os.path.exists(currentPath):
        return "no current Path"
    if os.path.isfile(currentPath):
        fileName = os.path.basename(currentPath)
        #return "&nbsp"*count + "|_ "+fileName+"</br>";
        return fileName;
    elif os.path.isdir(currentPath):
        #ret="&nbsp"*count + "|_ "+currentPath+"</br>"
        ret={currentPath:{}};
        pathList = os.listdir(currentPath)
        for eachPath in pathList:
            ret[currentPath][eachPath]=travelTree(currentPath + '/' + eachPath, count + 1)
        return ret;
    else :
        return "<br/>"



@router.Router("/"+baseUrl+"/explorer")
def explorer(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    
    return Template.View("admin/explorer.shtml",{});

def ListDic():
    jsonW={
      "authorityId": 1,
      "authorityName": "系统管理",
      "orderNumber": 1,
      "menuUrl": "null",
      "menuIcon": "layui-icon-set",
      "createTime": "2018/06/29 11:05:41",
      "authority": "null",
      "checked": 0,
      "updateTime": "2018/07/13 09:13:42",
      "isMenu": 0,
      "parentId": -1
    }

@router.Router("/"+baseUrl+"/sqlexec")
def sqlexec(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    dbNames=os.listdir(os.getcwd()+"/sqliteDB/");
    dbSel="";
    for dbName in dbNames:
        dbSel+="<option value='%s'  >%s</option>"%(dbName,dbName);
    return Template.View("admin/adminsqlexec.shtml",{"DatabaseSel":dbSel});

def SQLCallcommitExec(dbname,sqlcode):
    con=sqlite3.connect("sqliteDB/"+dbname);
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    con.commit();
    Infotr=con.total_changes;
    cur.close();
    con.close();
    return Infotr
def SQLCallExec(dbname,sqlcode):
    con=sqlite3.connect("sqliteDB/"+dbname);
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    col_name_list = [tuple[0] for tuple in cur.description]
    cur.close();
    con.close();
    retData=[];
    for item in retinfo:
        Data={};
        indexx=0;
        for filedName in col_name_list:
            Data[filedName]=item[indexx];
            indexx+=1;
        retData.append(Data);
    return retData;
@router.Router("/"+baseUrl+"/sqlexecCall")
def sqlexecCall(HttpRequest,Session):
    if('AuthCode' in Session.keys()):
        AuthCode=Session['AuthCode'];
        Username=Session["Username"];
        Success=CheckAuth(Username,AuthCode,HttpRequest.Remote_Addr);
        if not(Success):
            return HttpIO.HttpResponse("Login failed!");
    else:
        return HttpIO.HttpResponse("Login failed!");
    dbName=HttpRequest.GET["db"];
    sql=HttpRequest.GET["sql"];
    commit=int(HttpRequest.GET["commit"]);
    SQL=base64.b64decode(sql);
    PPLog(HttpRequest,Session,Username,"执行SQL语句:"+SQL.decode('UTF-8'));
    if(commit == 0):
        retData=SQLCallExec(dbName,SQL.decode('UTF-8'));
    elif(commit ==1):
        retData=[{'ChangeLine':SQLCallcommitExec(dbName,SQL.decode('UTF-8'))}];
    return HttpIO.HttpResponse(json.dumps(retData));
@router.Router("/"+baseUrl+"/explorerJson")
def explorerJson(HttpRequest,Session):
    #Files=travelTree("./");
    currentPath="./";
    #return HttpIO.HttpResponse(str(Files));
    pathList = os.listdir(currentPath)
    retJson=[];
    jsonW={
      "authorityId": 2,
      "filename": "用户管理",
      "orderNumber": 1,
      "menuUrl": "system/user",
      "menuIcon": "fa fa-file",
      "createTime": "2018/06/29 11:05:41",
      "authority": "null",
      "checked": 0,
      "updateTime": "2018/07/13 09:13:42",
      "isMenu": 0,
      "parentId": -1
    }
    i=1;
    fileJson=[];
    dicJson=[];
    for DicName in pathList:
        jsonW['authorityId']=i;
        if(os.path.isfile(DicName)):
            jsonW['isMenu']=0;
            jsonW['filename']=DicName;
            mtime = os.stat(currentPath+DicName).st_mtime
            ctime =os.stat(currentPath+DicName).st_ctime
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
            jsonW['createTime']=file_modify_time;
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            jsonW['updateTime']=file_modify_time;
            fileJson.append( copy.copy(jsonW));
        else:
            jsonW['isMenu']=1;
            jsonW['filename']=DicName;
            jsonW['menuUrl']="system/user";
            #jsonW['menuIcon']='layui-icon-file';
            mtime = os.stat(currentPath+DicName).st_mtime
            ctime =os.stat(currentPath+DicName).st_ctime
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
            jsonW['createTime']=file_modify_time;
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            jsonW['updateTime']=file_modify_time;
            dicJson.append(copy.copy(jsonW));
            #jsonW['isMenu']=0;
            #jsonW['parentId']=i;
            #jsonW['authorityId']=i*100;
            #dicJson.append(copy.copy(jsonW));
        i+=1;
    for i in dicJson:
        retJson.append(i);
    for i in fileJson:
        retJson.append(i);
    return Template.View("admin/menus.json",{"retJson":json.dumps(retJson)});




