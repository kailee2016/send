from dataCenterPackage import dataCenterVar as dv
from connectDB import gzdxDB as gd
import requests


def insertJzg(L):
    '''同步前将likai_sjtb_jzgxxb中的内容先清空,后插入'''
    if not dv.debug:
        con=gd.conn(gd.gzdx_connectString)
        cur=con.cursor()
        ##清空likai_sjtb_jzgxxb
        cur.execute('delete from likai_sjtb_jzgxxb')
        con.commit()
        #将数据中心的教师用户同步至jw数据库
        cur.executemany('insert into LIKAI_SJTB_JZGXXB(jgh_id,jgh,xm,xb,csrq,dqzt,zcmc,jgdm) values (:1,:2,:3,:4,:5,:6,:7,:8)',L)
        con.commit()
        #####备份
        t=cur.execute(dv.backUpExists).fetchone()[0]
        if t:
            cur.execute(dv.dropBackUpTable)
            con.commit()
        cur.execute(dv.backUpCode)
        gd.calProc(dv.updateAndinsertJzg,[0])
        cur.close()
        con.close()
        return 1
    else:
        return 0

def sytojs(max_index=25):
    '''接收数据中心的教师信息'''
    url=dv.baseUrl+dv.urlDir['tch']
    L=[]
    params=dv.params
    for index in range(1,max_index):
        params['page_index']=index
        #print(params)
        results=requests.get(url,params=params,headers=dv.headers).json()['result']
        for data in results:
            if data['O_STAFF_BASIC_PARENTORG_CODE']:
                jgh=data['O_STAFF_BASIC_STAFFID']
                jgh_id=jgh
                xm=data['O_STAFF_BASIC_NAME']
                xb=data['O_STAFF_BASIC_SEX_CODE']
                csrq=data['O_STAFF_BASIC_BIRTHDAY']
                dqzt=data['O_STAFF_BASIC_WORKSTATE_CODE']
                zcmc=data['O_STAFF_BASIC_MAJORQ']
                jgdm=data['O_STAFF_BASIC_ORG_CODE']
                L.append((jgh_id,jgh,xm,xb,csrq,dqzt,zcmc,jgdm))
    return insertJzg(L)

