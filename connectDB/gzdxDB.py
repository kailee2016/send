import cx_Oracle as co
import sqlite3
import os
import openpyxl 
###setting insert into the sqlite database###########
#sqliteInsertCode='''insert into logs values ('{}','{}','{}','{}','{}')'''

##########Set Base Connect String###########
gzdx_connectString='gzdx_jw_user/Gzhu2018!!@172.17.100.30:1521/gzdx'
sqlite_connectString='D:\\send'+'\\logs.sqlite3'

def conn(connectString=''):
    '''连接数据库,connectString=userName/userPass@ip:port/sid'''
    try:
        return co.connect(connectString,encoding="UTF-8")
    except:
        raise ValueError("can not connect to database")
def consqlite():
    '''连接发送失败数据库'''
    try:
        con=sqlite3.connect(sqlite_connectString)
        #print(con)
        return con
    except:
        raise ValueError("can not connect to database")

##############get data from database##################
def getData(queryString):
    con=conn(gzdx_connectString)
    cur=con.cursor()
    data=cur.execute(queryString).fetchall()
    cur.close()
    con.close()
    return data

####################insert into the send log######################
def insertSqlite(queryString):
    '''插入发送日志,queryString为元祖列表'''
    queryString=tuple(queryString)
    #print(queryString)
    con=consqlite()
    cur=con.cursor()
    cur.executemany("insert into logs values(?,?,?,?,?)",queryString)
    cur.close()
    con.commit()
    con.close()

def getXlsData(fileName):
    wb=''
    path=r'D:\back\send\files'
    #print(path)
    if os.path.exists(path+'\\'+fileName):
        fileName=path+'\\'+fileName
        wb=openpyxl.load_workbook(fileName)
    return wb
 ##########################################

def calProc(procName,procParas):
    '''调用存储过程'''
    sign=0
    if procName:
        con=conn(gzdx_connectString)
        cur=con.cursor()
        cur.callproc(procName,procParas)
        con.commit()
        cur.close()
        con.close()
        sign=1
    else:
        pass
    return sign
    
           
