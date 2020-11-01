#encoding:utf-8
#此程序用于生成 数据库表类 类静态方法当中配有CRUD
import sqlite3;
import sys;
import os;
dbCModel="""#encoding:utf-8
import sqlite3;
import urllib;
import uuid;
import time;
def commitExec(sqlcode):
    con=sqlite3.connect("{{DatabaseFileName}}");
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    con.commit();
    Infotr=con.total_changes;
    cur.close();
    con.close();
    return Infotr
def Exec(sqlcode):
    con=sqlite3.connect("{{DatabaseFileName}}");
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    cur.close();
    con.close();
    return retinfo;
""";

fileModel="""#encoding:utf-8
import urllib;
from Lib.dbC import {{DatabaseName}}
baseObject={{DatabaseName}};
tables={{TableNames}};
""";
classModel="""
class {{TableName}}:
{{StaticFiledDefine}}
    TableFileds=[{{FiledNamesString}}]
    def __init__(self):
{{FiledNamesDefine}}
    #Read Datas;
    @staticmethod
    def Select({{FiledNamesParametersDefine}},Limit={'Enable':False,'orderby':{{LimitDefaultFiled}},'index':0,'length':0,'desc':False},DataMethod={'Enable':False,'FiledName':{{LimitDefaultFiled}},'Method':'Count' }):
        WhereFiledsKeys=[{{FiledNamesString}}];
        WhereFiledsValues=[{{FiledNameParamters}}];
        WhereSQL="where ";
        WhereCount=0;
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+str(WhereFiledsValues[FiledIndex])+"'" );
                WhereCount+=1;
        orderbySQL=""
        if(Limit['Enable']==True):
            orderbySQL=" order by "+Limit['orderby']+(" desc " if Limit['desc'] else " ")+" limit "+str(Limit['index'])+","+str(Limit['length'])
        sqlcode="select "+( DataMethod['Method']+"("+DataMethod['FiledName']+")"  if DataMethod['Enable']  else '*' )+" from {{TableName}} "+(WhereSQL if WhereCount>0 else "" )+orderbySQL+";";
        Datalist=baseObject.Exec(sqlcode);
        if(DataMethod['Enable']):
            return Datalist[0][0]
        FiledNamesStr=[{{FiledNamesString}}];
        retSelectList=[];
        for FiledData in Datalist:
            CurDataObj={{TableName}}();
            for FiledNameIndex in range(len(FiledNamesStr)):
                attrName=FiledNamesStr[FiledNameIndex];
                attrValue=FiledData[FiledNameIndex];
                setattr(CurDataObj,attrName,attrValue);
            retSelectList.append(CurDataObj);
        return retSelectList;
    #Create Datas; Paramters = List<{{TableName}}>
    @staticmethod
    def Insert({{TableName}}List):
        InsertList={{TableName}}List;
        if(type(InsertList) != list):
            raise Exception("Paramter is list");
        Sqlcodes=[];
        FiledNamesStr=[{{FiledNamesString}}];
        for InsertObj in InsertList:
            insertFiledStr=[];
            insertFiledValue=[];
            for Filed in FiledNamesStr:
                FiledName=Filed;
                FiledValue=getattr(InsertObj,FiledName);
                if(FiledValue ==None):
                    continue;
                insertFiledStr.append(FiledName);
                insertFiledValue.append(FiledValue);
            Sqlcodes.append("INSERT INTO {{TableName}} %s values %s ;"%(str(tuple(insertFiledStr)).replace("'",""),str(tuple(insertFiledValue))));
        for sqlcode in Sqlcodes:
            Success=baseObject.commitExec(sqlcode);
            if(Success!=1):
                raise Exception("Insert error:",sqlcode);
        return True;
    def Update(self,{{FiledNamesParametersDefine}}):
        FiledNamesStr=[{{FiledNamesString}}];
        UpdateFiledsValues=[{{FiledNameParamters}}];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            par=getattr(self,WhereFiled);
            if(par == None):
                par = '';
            WhereFiledsValues.append(str(par));
        WhereFiledsKeys=[{{FiledNamesString}}];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        SetCount=0;
        SetSQL="";
        for UpdateFiledIndex in range(len(UpdateFiledsValues)):
            if(UpdateFiledsValues[UpdateFiledIndex] != None and UpdateFiledsValues[UpdateFiledIndex] !="" ):
                SetFiledName=FiledNamesStr[UpdateFiledIndex];
                SetFiledValue=UpdateFiledsValues[UpdateFiledIndex];
                SetSQL+=SetFiledName+"='"+str(SetFiledValue)+"',";
                SetCount+=1;
        if(SetCount<=0):
            return False;
        SetSQL=SetSQL[:-1];
        CommitSQL="UPDATE {{TableName}} SET "+SetSQL+" "+WhereSQL;
        Success=baseObject.commitExec(CommitSQL);
        if(Success == 1):
            return True;
        return False;
    def Delete(self):
        FiledNamesStr=[{{FiledNamesString}}];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            par=getattr(self,WhereFiled);
            if(par == None):
                par = '';
            WhereFiledsValues.append(str(par));
        WhereFiledsKeys=[{{FiledNamesString}}];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        sqlcode=("DELETE FROM {{TableName}}"+WhereSQL+";");
        Success=baseObject.commitExec(sqlcode);
        if(Success==1):
            return True;
        return False;
                
""";
dbFileName=(sys.argv[1]);
print("Database-FileName:",dbFileName);
def Exec(sqlcode):
    con=sqlite3.connect(dbFileName);
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    cur.close();
    con.close();
    return retinfo;

tablesR=(Exec("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"));
NotTableName=["sqlite_sequence"];
tableNames=[];
for tableName in tablesR:
    tableName=tableName[0];
    if not(tableName in NotTableName):
        tableNames.append(tableName);
#print("tables:",tableNames);
FiledNameList={};
for tbName in tableNames:
    FiledNames=[];
    print("Create python class For:"+tbName);
    for FiledAttr in (Exec("PRAGMA table_info(%s);"%(tbName))):
        FiledNames.append({"FiledName":FiledAttr[1],"NotNull":bool(FiledAttr[3])});
        print("\t Create Filed:"+FiledAttr[1]);
    FiledNameList[tbName]=FiledNames;
#print(FiledNameList);
def RpTemplate(Content,datas={}):
    for key in datas.keys():
        Content=Content.replace("{{%s}}"%(key),datas[key]);
    return Content;
def Save(FileName,Content):
    fp=open(FileName,"wb");
    fp.write(bytes(Content,encoding="UTF-8"));
    fp.close();

DatabaseName=os.path.basename(dbFileName)[:-3];

#下面这个模板生成的代码要保存到 Lib\dbC\目录下 名称应为数据库名
DbCFileContent=RpTemplate(dbCModel,{"DatabaseFileName":dbFileName});
#下面这个代码要保存到Dal\目录下 名称应为数据库名
dbModel= RpTemplate(fileModel,{"DatabaseName":DatabaseName,"TableNames":str(tableNames)});
for tbName in tableNames:
    FiledNamesDefine="";
    FiledNamesParametersDefine="";
    FiledNamesString="";
    FiledNameParamters="";
    StaticFiledDefine="";
    for FiledAttr in FiledNameList[tbName]:
        FiledNamesDefine+="        self."+str(FiledAttr["FiledName"])+"=None\n";
        StaticFiledDefine+="    "+str(FiledAttr["FiledName"])+"='%s'\n"%(FiledAttr["FiledName"]);
        FiledNamesParametersDefine+=FiledAttr["FiledName"]+("=''" if (FiledAttr["NotNull"]) else "=None" )+",";
        FiledNamesString+="'"+FiledAttr["FiledName"]+"',";
        FiledNameParamters+=FiledAttr["FiledName"]+",";
    FiledNamesParametersDefine=FiledNamesParametersDefine[:-1];
    #LimitDefaultFiled=tbName+"."+FiledNameList[tbName][0]["FiledName"];
    LimitDefaultFiled=FiledNameList[tbName][0]["FiledName"];
    FiledNamesString=FiledNamesString[:-1];
    FiledNameParamters=FiledNameParamters[:-1];
    tmpJdbModel = RpTemplate(classModel,{"LimitDefaultFiled":LimitDefaultFiled,"StaticFiledDefine":StaticFiledDefine,"TableName":tbName,"FiledNamesDefine":FiledNamesDefine,"FiledNameParamters":FiledNameParamters,"FiledNamesParametersDefine":FiledNamesParametersDefine,"FiledNamesString":FiledNamesString});
    dbModel+=tmpJdbModel;

Save("Lib\\dbC\\"+DatabaseName+".py",DbCFileContent);
Save("Dal\\"+DatabaseName+".py",dbModel);
