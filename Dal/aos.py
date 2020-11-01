#encoding:utf-8
import urllib;
from Lib.dbC import aos
baseObject=aos;
tables=['SystemSetting', 'adminAuth', 'adminLoginLogs', 'adminOpradeLog', 'adminUserInfo'];

class SystemSetting:
    Key='Key'
    Value='Value'

    TableFileds=['Key','Value']
    def __init__(self):
        self.Key=None
        self.Value=None

    #Read Datas;
    @staticmethod
    def Select(Key='',Value='',Limit={'Enable':False,'orderby':Key,'index':0,'length':0,'desc':False},DataMethod={'Enable':False,'FiledName':Key,'Method':'Count' }):
        WhereFiledsKeys=['Key','Value'];
        WhereFiledsValues=[Key,Value];
        WhereSQL="where ";
        WhereCount=0;
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+str(WhereFiledsValues[FiledIndex])+"'" );
                WhereCount+=1;
        orderbySQL=""
        if(Limit['Enable']==True):
            orderbySQL="order by "+Limit['orderby']+(" desc " if Limit['desc'] else " ")+" limit "+str(Limit['index'])+","+str(Limit['length'])
        sqlcode="select "+( DataMethod['Method']+"("+DataMethod['FiledName']+")"  if DataMethod['Enable']  else '*' )+" from SystemSetting "+(WhereSQL if WhereCount>0 else "" )+orderbySQL+";";
        Datalist=baseObject.Exec(sqlcode);
        if(DataMethod['Enable']):
            return Datalist[0][0]
        FiledNamesStr=['Key','Value'];
        retSelectList=[];
        for FiledData in Datalist:
            CurDataObj=SystemSetting();
            for FiledNameIndex in range(len(FiledNamesStr)):
                attrName=FiledNamesStr[FiledNameIndex];
                attrValue=FiledData[FiledNameIndex];
                setattr(CurDataObj,attrName,attrValue);
            retSelectList.append(CurDataObj);
        return retSelectList;
    #Create Datas; Paramters = List<SystemSetting>
    @staticmethod
    def Insert(SystemSettingList):
        InsertList=SystemSettingList;
        if(type(InsertList) != list):
            raise Exception("Paramter is list");
        Sqlcodes=[];
        FiledNamesStr=['Key','Value'];
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
            Sqlcodes.append("INSERT INTO SystemSetting %s values %s ;"%(str(tuple(insertFiledStr)).replace("'",""),str(tuple(insertFiledValue))));
        for sqlcode in Sqlcodes:
            Success=baseObject.commitExec(sqlcode);
            if(Success!=1):
                raise Exception("Insert error:",sqlcode);
        return True;
    def Update(self,Key='',Value=''):
        FiledNamesStr=['Key','Value'];
        UpdateFiledsValues=[Key,Value];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['Key','Value'];
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
        CommitSQL="UPDATE SystemSetting SET "+SetSQL+" "+WhereSQL;
        Success=baseObject.commitExec(CommitSQL);
        if(Success == 1):
            return True;
        return False;
    def Delete(self):
        FiledNamesStr=['Key','Value'];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['Key','Value'];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        sqlcode=("DELETE FROM SystemSetting"+WhereSQL+";");
        Success=baseObject.commitExec(sqlcode);
        if(Success==1):
            return True;
        return False;
                

class adminAuth:
    id='id'
    AuthKey='AuthKey'
    Username='Username'
    ip='ip'
    AuthDateTime='AuthDateTime'

    TableFileds=['id','AuthKey','Username','ip','AuthDateTime']
    def __init__(self):
        self.id=None
        self.AuthKey=None
        self.Username=None
        self.ip=None
        self.AuthDateTime=None

    #Read Datas;
    @staticmethod
    def Select(id='',AuthKey='',Username='',ip='',AuthDateTime='',Limit={'Enable':False,'orderby':id,'index':0,'length':0,'desc':False},DataMethod={'Enable':False,'FiledName':id,'Method':'Count' }):
        WhereFiledsKeys=['id','AuthKey','Username','ip','AuthDateTime'];
        WhereFiledsValues=[id,AuthKey,Username,ip,AuthDateTime];
        WhereSQL="where ";
        WhereCount=0;
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+str(WhereFiledsValues[FiledIndex])+"'" );
                WhereCount+=1;
        orderbySQL=""
        if(Limit['Enable']==True):
            orderbySQL="order by "+Limit['orderby']+(" desc " if Limit['desc'] else " ")+" limit "+str(Limit['index'])+","+str(Limit['length'])
        sqlcode="select "+( DataMethod['Method']+"("+DataMethod['FiledName']+")"  if DataMethod['Enable']  else '*' )+" from adminAuth "+(WhereSQL if WhereCount>0 else "" )+orderbySQL+";";
        Datalist=baseObject.Exec(sqlcode);
        if(DataMethod['Enable']):
            return Datalist[0][0]
        FiledNamesStr=['id','AuthKey','Username','ip','AuthDateTime'];
        retSelectList=[];
        for FiledData in Datalist:
            CurDataObj=adminAuth();
            for FiledNameIndex in range(len(FiledNamesStr)):
                attrName=FiledNamesStr[FiledNameIndex];
                attrValue=FiledData[FiledNameIndex];
                setattr(CurDataObj,attrName,attrValue);
            retSelectList.append(CurDataObj);
        return retSelectList;
    #Create Datas; Paramters = List<adminAuth>
    @staticmethod
    def Insert(adminAuthList):
        InsertList=adminAuthList;
        if(type(InsertList) != list):
            raise Exception("Paramter is list");
        Sqlcodes=[];
        FiledNamesStr=['id','AuthKey','Username','ip','AuthDateTime'];
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
            Sqlcodes.append("INSERT INTO adminAuth %s values %s ;"%(str(tuple(insertFiledStr)).replace("'",""),str(tuple(insertFiledValue))));
        for sqlcode in Sqlcodes:
            Success=baseObject.commitExec(sqlcode);
            if(Success!=1):
                raise Exception("Insert error:",sqlcode);
        return True;
    def Update(self,id='',AuthKey='',Username='',ip='',AuthDateTime=''):
        FiledNamesStr=['id','AuthKey','Username','ip','AuthDateTime'];
        UpdateFiledsValues=[id,AuthKey,Username,ip,AuthDateTime];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['id','AuthKey','Username','ip','AuthDateTime'];
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
        CommitSQL="UPDATE adminAuth SET "+SetSQL+" "+WhereSQL;
        Success=baseObject.commitExec(CommitSQL);
        if(Success == 1):
            return True;
        return False;
    def Delete(self):
        FiledNamesStr=['id','AuthKey','Username','ip','AuthDateTime'];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['id','AuthKey','Username','ip','AuthDateTime'];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        sqlcode=("DELETE FROM adminAuth"+WhereSQL+";");
        Success=baseObject.commitExec(sqlcode);
        if(Success==1):
            return True;
        return False;
                

class adminLoginLogs:
    ID='ID'
    username='username'
    LoginTime='LoginTime'
    IP='IP'

    TableFileds=['ID','username','LoginTime','IP']
    def __init__(self):
        self.ID=None
        self.username=None
        self.LoginTime=None
        self.IP=None

    #Read Datas;
    @staticmethod
    def Select(ID='',username='',LoginTime='',IP='',Limit={'Enable':False,'orderby':ID,'index':0,'length':0,'desc':False},DataMethod={'Enable':False,'FiledName':ID,'Method':'Count' }):
        WhereFiledsKeys=['ID','username','LoginTime','IP'];
        WhereFiledsValues=[ID,username,LoginTime,IP];
        WhereSQL="where ";
        WhereCount=0;
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+str(WhereFiledsValues[FiledIndex])+"'" );
                WhereCount+=1;
        orderbySQL=""
        if(Limit['Enable']==True):
            orderbySQL="order by "+Limit['orderby']+(" desc " if Limit['desc'] else " ")+" limit "+str(Limit['index'])+","+str(Limit['length'])
        sqlcode="select "+( DataMethod['Method']+"("+DataMethod['FiledName']+")"  if DataMethod['Enable']  else '*' )+" from adminLoginLogs "+(WhereSQL if WhereCount>0 else "" )+orderbySQL+";";
        Datalist=baseObject.Exec(sqlcode);
        if(DataMethod['Enable']):
            return Datalist[0][0]
        FiledNamesStr=['ID','username','LoginTime','IP'];
        retSelectList=[];
        for FiledData in Datalist:
            CurDataObj=adminLoginLogs();
            for FiledNameIndex in range(len(FiledNamesStr)):
                attrName=FiledNamesStr[FiledNameIndex];
                attrValue=FiledData[FiledNameIndex];
                setattr(CurDataObj,attrName,attrValue);
            retSelectList.append(CurDataObj);
        return retSelectList;
    #Create Datas; Paramters = List<adminLoginLogs>
    @staticmethod
    def Insert(adminLoginLogsList):
        InsertList=adminLoginLogsList;
        if(type(InsertList) != list):
            raise Exception("Paramter is list");
        Sqlcodes=[];
        FiledNamesStr=['ID','username','LoginTime','IP'];
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
            Sqlcodes.append("INSERT INTO adminLoginLogs %s values %s ;"%(str(tuple(insertFiledStr)).replace("'",""),str(tuple(insertFiledValue))));
        for sqlcode in Sqlcodes:
            Success=baseObject.commitExec(sqlcode);
            if(Success!=1):
                raise Exception("Insert error:",sqlcode);
        return True;
    def Update(self,ID='',username='',LoginTime='',IP=''):
        FiledNamesStr=['ID','username','LoginTime','IP'];
        UpdateFiledsValues=[ID,username,LoginTime,IP];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['ID','username','LoginTime','IP'];
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
        CommitSQL="UPDATE adminLoginLogs SET "+SetSQL+" "+WhereSQL;
        Success=baseObject.commitExec(CommitSQL);
        if(Success == 1):
            return True;
        return False;
    def Delete(self):
        FiledNamesStr=['ID','username','LoginTime','IP'];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['ID','username','LoginTime','IP'];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        sqlcode=("DELETE FROM adminLoginLogs"+WhereSQL+";");
        Success=baseObject.commitExec(sqlcode);
        if(Success==1):
            return True;
        return False;
                

class adminOpradeLog:
    id='id'
    OpradeContent='OpradeContent'
    ip='ip'
    OpradeUsername='OpradeUsername'
    OpradeDateTime='OpradeDateTime'

    TableFileds=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime']
    def __init__(self):
        self.id=None
        self.OpradeContent=None
        self.ip=None
        self.OpradeUsername=None
        self.OpradeDateTime=None

    #Read Datas;
    @staticmethod
    def Select(id='',OpradeContent='',ip='',OpradeUsername='',OpradeDateTime='',Limit={'Enable':False,'orderby':id,'index':0,'length':0,'desc':False},DataMethod={'Enable':False,'FiledName':id,'Method':'Count' }):
        WhereFiledsKeys=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
        WhereFiledsValues=[id,OpradeContent,ip,OpradeUsername,OpradeDateTime];
        WhereSQL="where ";
        WhereCount=0;
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+str(WhereFiledsValues[FiledIndex])+"'" );
                WhereCount+=1;
        orderbySQL=""
        if(Limit['Enable']==True):
            orderbySQL="order by "+Limit['orderby']+(" desc " if Limit['desc'] else " ")+" limit "+str(Limit['index'])+","+str(Limit['length'])
        sqlcode="select "+( DataMethod['Method']+"("+DataMethod['FiledName']+")"  if DataMethod['Enable']  else '*' )+" from adminOpradeLog "+(WhereSQL if WhereCount>0 else "" )+orderbySQL+";";
        Datalist=baseObject.Exec(sqlcode);
        if(DataMethod['Enable']):
            return Datalist[0][0]
        FiledNamesStr=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
        retSelectList=[];
        for FiledData in Datalist:
            CurDataObj=adminOpradeLog();
            for FiledNameIndex in range(len(FiledNamesStr)):
                attrName=FiledNamesStr[FiledNameIndex];
                attrValue=FiledData[FiledNameIndex];
                setattr(CurDataObj,attrName,attrValue);
            retSelectList.append(CurDataObj);
        return retSelectList;
    #Create Datas; Paramters = List<adminOpradeLog>
    @staticmethod
    def Insert(adminOpradeLogList):
        InsertList=adminOpradeLogList;
        if(type(InsertList) != list):
            raise Exception("Paramter is list");
        Sqlcodes=[];
        FiledNamesStr=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
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
            Sqlcodes.append("INSERT INTO adminOpradeLog %s values %s ;"%(str(tuple(insertFiledStr)).replace("'",""),str(tuple(insertFiledValue))));
        for sqlcode in Sqlcodes:
            Success=baseObject.commitExec(sqlcode);
            if(Success!=1):
                raise Exception("Insert error:",sqlcode);
        return True;
    def Update(self,id='',OpradeContent='',ip='',OpradeUsername='',OpradeDateTime=''):
        FiledNamesStr=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
        UpdateFiledsValues=[id,OpradeContent,ip,OpradeUsername,OpradeDateTime];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
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
        CommitSQL="UPDATE adminOpradeLog SET "+SetSQL+" "+WhereSQL;
        Success=baseObject.commitExec(CommitSQL);
        if(Success == 1):
            return True;
        return False;
    def Delete(self):
        FiledNamesStr=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['id','OpradeContent','ip','OpradeUsername','OpradeDateTime'];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        sqlcode=("DELETE FROM adminOpradeLog"+WhereSQL+";");
        Success=baseObject.commitExec(sqlcode);
        if(Success==1):
            return True;
        return False;
                

class adminUserInfo:
    ID='ID'
    Username='Username'
    Password='Password'
    Mode='Mode'

    TableFileds=['ID','Username','Password','Mode']
    def __init__(self):
        self.ID=None
        self.Username=None
        self.Password=None
        self.Mode=None

    #Read Datas;
    @staticmethod
    def Select(ID='',Username='',Password='',Mode='',Limit={'Enable':False,'orderby':ID,'index':0,'length':0,'desc':False},DataMethod={'Enable':False,'FiledName':ID,'Method':'Count' }):
        WhereFiledsKeys=['ID','Username','Password','Mode'];
        WhereFiledsValues=[ID,Username,Password,Mode];
        WhereSQL="where ";
        WhereCount=0;
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+str(WhereFiledsValues[FiledIndex])+"'" );
                WhereCount+=1;
        orderbySQL=""
        if(Limit['Enable']==True):
            orderbySQL="order by "+Limit['orderby']+(" desc " if Limit['desc'] else " ")+" limit "+str(Limit['index'])+","+str(Limit['length'])
        sqlcode="select "+( DataMethod['Method']+"("+DataMethod['FiledName']+")"  if DataMethod['Enable']  else '*' )+" from adminUserInfo "+(WhereSQL if WhereCount>0 else "" )+orderbySQL+";";
        Datalist=baseObject.Exec(sqlcode);
        if(DataMethod['Enable']):
            return Datalist[0][0]
        FiledNamesStr=['ID','Username','Password','Mode'];
        retSelectList=[];
        for FiledData in Datalist:
            CurDataObj=adminUserInfo();
            for FiledNameIndex in range(len(FiledNamesStr)):
                attrName=FiledNamesStr[FiledNameIndex];
                attrValue=FiledData[FiledNameIndex];
                setattr(CurDataObj,attrName,attrValue);
            retSelectList.append(CurDataObj);
        return retSelectList;
    #Create Datas; Paramters = List<adminUserInfo>
    @staticmethod
    def Insert(adminUserInfoList):
        InsertList=adminUserInfoList;
        if(type(InsertList) != list):
            raise Exception("Paramter is list");
        Sqlcodes=[];
        FiledNamesStr=['ID','Username','Password','Mode'];
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
            Sqlcodes.append("INSERT INTO adminUserInfo %s values %s ;"%(str(tuple(insertFiledStr)).replace("'",""),str(tuple(insertFiledValue))));
        for sqlcode in Sqlcodes:
            Success=baseObject.commitExec(sqlcode);
            if(Success!=1):
                raise Exception("Insert error:",sqlcode);
        return True;
    def Update(self,ID='',Username='',Password='',Mode=''):
        FiledNamesStr=['ID','Username','Password','Mode'];
        UpdateFiledsValues=[ID,Username,Password,Mode];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['ID','Username','Password','Mode'];
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
        CommitSQL="UPDATE adminUserInfo SET "+SetSQL+" "+WhereSQL;
        Success=baseObject.commitExec(CommitSQL);
        if(Success == 1):
            return True;
        return False;
    def Delete(self):
        FiledNamesStr=['ID','Username','Password','Mode'];
        WhereFiledsValues=[];
        for WhereFiled in FiledNamesStr:
            WhereFiledsValues.append(str(getattr(self,WhereFiled)));
        WhereFiledsKeys=['ID','Username','Password','Mode'];
        WhereSQL="";
        WhereCount=0
        for FiledIndex in range(len(WhereFiledsValues)):
            if(WhereFiledsValues[FiledIndex] != None and WhereFiledsValues[FiledIndex] !="" ):
                WhereSQL+=(" and " if WhereCount>0 else " where ")+WhereFiledsKeys[FiledIndex]+(WhereFiledsValues[FiledIndex] if(WhereFiledsValues[FiledIndex][0]=="<" or WhereFiledsValues[FiledIndex][0]==">")else "="+"'"+WhereFiledsValues[FiledIndex]+"'" );
                WhereCount+=1;
        sqlcode=("DELETE FROM adminUserInfo"+WhereSQL+";");
        Success=baseObject.commitExec(sqlcode);
        if(Success==1):
            return True;
        return False;
                
