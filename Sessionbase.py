import sqlite3;
import urllib;
import uuid;
import time;
import re;
sysdb="systeminfo.db";
def commitExec(sqlcode):
    #websiteLog.LogSQLCODE(sqlcode);
    con=sqlite3.connect(sysdb);
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    con.commit();
    Infotr=con.total_changes;
    cur.close();
    con.close();
    return Infotr#retinfo;
def Exec(sqlcode):
    #websiteLog.LogSQLCODE(sqlcode);
    con=sqlite3.connect(sysdb);
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    cur.close();
    con.close();
    #print sqlcode;
    return retinfo;

def GetSession(SessionID):
    SessionID =re.findall("(([A-Z]|[a-z]|[0-9])+)",SessionID)[0][0];
    return Exec("select * from Session where key='%s';"%(SessionID))[0][1];
def WriteSession(SessionID,Session):
    SessionID =re.findall("(([A-Z]|[a-z]|[0-9])+)",SessionID)[0][0];
    return commitExec("""INSERT INTO Session ([Key],Value) VALUES ('%s',"%s");"""%(SessionID,str(Session)))
def UpdateSession(SessionID,Session):
    SessionID=re.findall("(([A-Z]|[a-z]|[0-9])+)",SessionID)[0][0];
    return commitExec("""UPDATE Session SET  Value = "%s" WHERE Key = '%s'"""%(str(Session),SessionID));