
#############
############this file is read the xls files,and then send the message
##############the xls file format is three columns ,user,content,sendtime
from connectDB import gzdxDB as gd
from msgPackage import gzdxdbEVENTS as gdb
import datetime
import uuid
def dealXls(jgDay,xxlx='xlsx01',fileName='sf.xlsx'):
    if fileName:
        sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res=gd.getXlsData(fileName)
        L=[]
        try:
            ws=res.get_sheet_by_name('Sheet1')
        except:
            ws=res.get_sheet_by_name('sheet1')
        #print(ws.max_row)
        for r in range(1,ws.max_row+1):
            user=str(ws.cell(r,1).value)
            title=gdb.setTitle(xxlx)
            content=str(ws.cell(r,2).value)
            # print(gdb.getNextDay(jgDay))
            # print(ws.cell(r,3).value)
            # print(type(ws.cell(r,3).value))
            if gdb.getNextDay(jgDay)==ws.cell(r,3).value:
                t=gdb.sendAndWrite(user,title,content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    if L:
        gd.insertSqlite(L)
    else:
        pass
    return L