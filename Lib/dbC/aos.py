#encoding:utf-8
import sqlite3;
import urllib;
import uuid;
import time;
def commitExec(sqlcode):
    con=sqlite3.connect("sqliteDB/aos.db");
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    con.commit();
    Infotr=con.total_changes;
    cur.close();
    con.close();
    return Infotr
def Exec(sqlcode):
    con=sqlite3.connect("sqliteDB/aos.db");
    cur=con.cursor();
    retinfo=cur.execute(sqlcode).fetchall();
    cur.close();
    con.close();
    return retinfo;
