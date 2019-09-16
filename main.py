from msgPackage import gzdxdbEVENTS as gde, gzdxProcEvents as gpe, gzdxVAR as gv, gzdxxlsEvents as gls
from dataCenterPackage import dataCenterEvents as dce
import datetime
###############xxlx,01,课表发送教师,02，课表发向学生,
##############03,学籍异动信息（向教师），03-1（学籍异动向学生）,
##############04,场地借用，07，调停课向教师,
##############05，学生考试，06，教师监考
#############08调停课向学生
#############09缓考消息
#############10选课提醒
#############11成绩录入提醒
#############12向学生发送成绩提醒
#############13慕课修读提醒消息
#############14学业预警消息
#############15成绩作废提醒
#############16教学班停开信息

admin='103667'

def xsOnceMsg():
    ####向学生发送一次性的消息
    ####xxlx=13,视频课修读网址
    xxlx='13'
    count = gde.dealData(gv.otherJgDay, xxlx=xxlx)
    #向学生发送成绩作废提醒
    gde.sendAndWrite(admin, '', '完成1-14')
    xxlx='15'
    gde.dealData(gv.otherJgDay,xxlx=xxlx)

def xsmain():
    '''主要是向学生发送'''
    xxlx='02'#课表发向学生
    count = gde.dealData(gv.keBiaoJgDay, xxlx=xxlx)
    xxlx='05'#学生考试信息
    count = gde.dealData(gv.ksJgDay, xxlx=xxlx)
    for xxlx in ['08','12']:
        count = gde.dealData(gv.otherJgDay, xxlx=xxlx)
    for nj in gv.xkTxNj:#提醒学生选课
        count=gde.dealData(nj,xxlx='10')
    xsOnceMsg()

def main():
    ## #xxlx=01,课表发送至教师,xxlx='02',课表发送至学生
    for xxlx in ['01']:
        count=gde.dealData(gv.keBiaoJgDay,xxlx=xxlx)
    ##xxlx=03,031,学籍异动消息发送
    for xxlx in ['03','031','04','07','09','14','16']:
        count=gde.dealData(gv.otherJgDay,xxlx=xxlx)
    for xxlx in ['06']:#考试信息
        count=gde.dealData(gv.ksJgDay,xxlx=xxlx)
    #在成绩结束的时间范围内，当天发,提醒教师录入成绩
    count=gde.dealData(gv.otherJgDay,xxlx='11')
    #发送外表数据当天发
    count=gls.dealXls(gv.otherJgDay)
    sign=gpe.update_jd()
    ## if sign:
    ##     gde.sendAndWrite(admin,'title','绩点\学业预警信息更新完成！')
    # ####以下为与数据中心同步结构,每两天更新一次
    sign=dce.sytojs()##常规情形下只会同步教师
    xsmain()
    gde.sendAndWrite(admin, '', '完成')
if __name__=='__main__':
    main()
