from msgPackage import gzdxVAR as gv,gzdxVAR2 as gv2
from msgInterface import send
from connectDB import gzdxDB as gd
import datetime
import uuid

def getBaseQuery(xxlx):
    queryString=''
    if xxlx=='01':
        queryString=gv.getNextDayKbCode
    if xxlx=='02':
        queryString=gv.getNextDayXsKbCode
    if xxlx=='03':
        queryString=gv.getXjYdxxCode
    if xxlx=='04':
        queryString=gv.getCdJyCode
    if xxlx=='05':
        queryString=gv.getXsKsCode
    if xxlx=='06':
        queryString=gv.getJsJkCode
    if xxlx=='07':
        queryString=gv.getJsTtkCode
    if xxlx=='08':
        queryString =gv.getXsTtkCode
    if xxlx=='09':
        queryString=gv.getXsHkCode
    if xxlx=='031':
        queryString=gv.getXjYdxxCode031
    if xxlx=='10':
        queryString=gv.getNjBxKcTxCode
    if xxlx=='11':
        queryString=gv.getJsLrCjTxCode
    if xxlx=='12':
         queryString=gv.getXscjCode
    if xxlx=='13':
        queryString=gv.getXsWlspk
    if xxlx=='14':
        queryString=gv.getXsXyYjCode
    if xxlx=='15':
        queryString=gv2.getNjZyXsxxCode
    if xxlx=='16':
        queryString=gv.getJsTkKcxx
    return queryString


def getNextDay(jgDay):
    '''获取发送消息的目标日期'''
    '''jgDay指目标日期与当前时间的间隔天数'''
    '''节假日课表替换可在此处设置'''
    if isinstance(jgDay,int):
        nowTime = datetime.datetime.now()
        txTime = (nowTime + datetime.timedelta(days=jgDay)).strftime('%Y-%m-%d')
    else:
        txTime=jgDay
    return txTime

def getZcXqj(jgDay):
    '''获取校历，元组（周次，星期几）,只返回第一行'''
    queryString=gv.getXtZcXqjSqlCode.format(getNextDay(jgDay))
    i=1
    while i<=1:
        data=gd.getData(queryString)[0]
        i=i+1
    return data


def setContentTemplate(xxlx):
    '''返回消息模板'''
    contentTemplate=''
    if xxlx=='01':
        contentTemplate="{}老师，您好！{}日（第{}周，星期{}），第{}，请您按时在{}，{}，{}室给{}讲授《{}》课程。详情可登陆教务系统查询，祝您工作愉快！"
    elif xxlx=='02':
        contentTemplate="{}同学，您好！{}日（第{}周，星期{}），第{}，请您按时在{}，{}室上《{}》课程。详情可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='031':
        contentTemplate="{}同学,您好!您办理的 “{}”,{},请关注您的个人课表信息，详情可与学院教务办公室联系，祝您学习愉快！"
    elif xxlx=='03':
        contentTemplate="{}老师，您好！您学院的{}同学办理的“{}”，{}，请关注该生的课表情况。祝您工作愉快！"
    elif xxlx=='04':
        contentTemplate="{}老师，您好!您申请使用的{},{}。详情可登陆教务系统查询，祝您工作愉快！"
    elif xxlx=='05':
        contentTemplate="{}同学,您好!您所修《{}》课程的考试时间为：{}，考试地点为{}，请携带相关证件准时参加，遵守考场纪律，考试作弊取消学位。详情可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='06':
        contentTemplate="{}老师，您好！请您准时在{}，{}，监考《{}》课程！温馨提醒，要先领试卷！祝您工作愉快！"
    elif xxlx=='07':
        contentTemplate="{}老师，您好!您办理的调停补课业务（课程：《{}》），{}。详细课表信息可登陆教务系统查询，祝您工作愉快！"
    elif xxlx=='08':
        contentTemplate="{}同学，您好！您的{}，详细课表信息可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='09':
        contentTemplate="{}同学，您好!您{}，{}，详情可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='10':
        contentTemplate="温馨提醒：{}同学，您好！根据您的年级专业教学计划，您还有{}等必修课程未选！如上述课程已选或已获学分，请忽略，学期应选课程要求，学分要求等可以向学生所在学院教学办公室联系，祝您学习愉快!"
    elif xxlx=='11':
        contentTemplate="温馨提醒：{}老师,您好!距您的教学班:{}的成绩提交{}"
    elif xxlx=='12':
        contentTemplate="{}同学，您好！您今天有新成绩进入，成绩概要信息为{},详细信息可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='13':
        contentTemplate="温馨提醒：{}同学，您好！您所选《{}》课程，选课结果已经进入{},请及时登录、按课程要求进行修读与考核，忘记密码可联系平台客服！(如已参与学习，请忽略该条消息）"
    elif xxlx=='14':
        contentTemplate="{}同学，您好!您{}，详情可登陆教务系统查询或与学生学院教学办公室沟通，祝您学习愉快！"
    elif xxlx=='15':
        contentTemplate='''温馨提醒，成绩作废申请将在{}-{}时间段内开放！注意：1）如果一门课程您需要或必须要被保留，那么您不需要对该门课程的任何成绩进行作废，相反如果一门课程您完全不需要，那么您需要对该门课程的所有成绩进行作废；2）作废后的成绩不可找回，请您谨慎申请；3）申请时，请检查您的申请是否处于保存状态，如是，请妥善决定是提交还是撤销，详情可与学生学院联系，祝您学习愉快！'''
    elif xxlx=='16':
        contentTemplate='''{}老师，您好！您的{}，祝您工作愉快！'''
    else:
        pass
    return contentTemplate+gv.messageComments
def lrCjTxPara(jgDay):
    data=''
    if jgDay>0:
        data='已不足{}天，请您及时录入、提交该教学班成绩,如您已提交或正在录入，请忽略该条信息！祝您工作愉快！'.format(jgDay)
    elif jgDay==0:
        data='须于今日完成，请您尽快提交该教学班成绩,如您已提交或正在录入，请忽略该条信息！祝您工作愉快！'
    elif jgDay<0:
        data='已滞后{}天，请尽快联系各学院教务办公室,如您已提交或正在录入，请忽略该条信息！祝您工作愉快！,'.format(abs(jgDay))
    else:
        pass
    return data

def setTitle(xxlx):
    ''''''
    if xxlx=='01' or xxlx=='02':
        return '【课表消息】'
    elif xxlx=='03' or xxlx=='031':
        return '【学籍异动消息】'
    elif xxlx=='04':
        return '【场地借用消息】'
    elif xxlx=='05' or xxlx=='06':
        return '【考试消息】'
    elif xxlx=='07' or xxlx=='08':
        return '【调课信息】'
    elif xxlx=='09':
        return '【缓考消息】'
    elif xxlx=='10':
        return '【选课消息】'
    elif xxlx in['11','12','15']:
        return '【成绩消息】'
    elif xxlx=='xlsx01':
        return '【学分费用消息】'
    elif xxlx=='13':
        return '【慕课修读消息】'
    elif xxlx=='14':
        return '【学业预警消息】'
    elif xxlx=='16':
        return '【教学任务信息】'
    else:
        return ''

def sendAndWrite(user,title,content):

    if gv.debug:
        t= send.LocalsendToUser(user, title, content)
    else:
        t = send.sendToUser(user, title, content)  # 发送
    return t


def dealData(jgDay,xxlx):
    ##nextDay,发送的目标日期，title，标题，content，内容
    nextDay=getNextDay(jgDay)
    title=setTitle(xxlx)
    contentTem=setContentTemplate(xxlx)
    L=[]
    baseQueryString=getBaseQuery(xxlx)
    if xxlx in ['01','02']:#课表,有多个周次，星期参数
        zcxqj=getZcXqj(jgDay)
        #print(type(zcxqj[0]))
        if xxlx in ['01','02'] and zcxqj[0] in gv.keBiaoZc:#在周次范围内，发送
            queryString=baseQueryString.format(zcxqj[0],zcxqj[1])
            #print(queryString)
            res=gd.getData(queryString)
            for data in res:
                if xxlx=='01':####jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc#####
                    user = data[0]  # '103885'#测试时
                    content = title + contentTem.format(data[1], nextDay, zcxqj[0], zcxqj[1], data[2], data[3], data[4],data[5], data[6], data[7])
                else:#jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc,xsxh,xsxm
                    user = data[8]  # '103885'#测试时
                    content = title + contentTem.format(data[9], nextDay, zcxqj[0], zcxqj[1], data[2], data[4], data[5],data[7])
                t=sendAndWrite(user,title,content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['10','13']:
        zcxqj=getZcXqj(0)
        if xxlx=='10':#选课提醒传递的是年级
            tDay = getNextDay(0)
            if tDay in gv.xkTxRq or (zcxqj[0] in gv.xkTxZc and zcxqj[1] in gv.xkTxXqj):
                queryString=baseQueryString.format(nextDay)
                res=gd.getData(queryString)
                for data in res:
                    user=data[0]
                    content = title + contentTem.format(data[1], data[2])
                    t=sendAndWrite(user,title,content)
                    sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        elif xxlx=='13':#慕课修读网址提醒
            if nextDay in gv.xkMkTxRq or(zcxqj[0] in gv.xkMkTxZc and zcxqj[1] in gv.xkMkTxXqj):
                queryString=baseQueryString
                res=gd.getData(queryString)
                for data in res:
                    user=data[0]
                    content=title+contentTem.format(data[1],data[2],data[3])
                    t=sendAndWrite(user,title,content)
                    sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        else:
            pass
    elif xxlx in ['03','031','04','05','06','07','08','09','12']:#只有日期一个参数
        #学籍异动发向学生与发向教务员不能是同一段代码 发向教师用03，发向学生用031
        if xxlx in ['12']:
            queryString=baseQueryString.format(gv.xsCjTxSfFsCjb,nextDay,nextDay)
            #print(queryString)
        else:
            queryString=baseQueryString.format(nextDay)
        res=gd.getData(queryString)
        for data in res:
            if xxlx=='031':
                if data[2] not in ['分方向（转入）', '大类分流（转入）']:
                    user = data[0]
                    content=title+contentTem.format(data[1],data[2],data[3])
            elif xxlx=='03':
                if data[2] not in ['分方向（转入）', '大类分流（转入）']:
                    user = data[4]  
                    content = title + contentTem.format(data[5], data[1], data[2], data[3])
            elif xxlx in ['04','07','09']:
                user=data[0]#'104660'#测试时
                content=title+contentTem.format(data[1],data[2],data[3])##
            elif xxlx in ['05']:
                user = data[0]  # '102813'
                content = title + contentTem.format(data[1], data[2], data[4], data[3])
            elif xxlx in ['06']:
                user=data[0]
                content = title + contentTem.format(data[1], data[2], data[3], data[4])
            elif xxlx in['08','12']:
                user = data[0]  # '104660'#测试时
                content = title + contentTem.format(data[1], data[2])
            else:
                user=None
                content=None
            if user:
                t=sendAndWrite(user, title, content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['11','14']:#无日期时间参数
        queryString=baseQueryString
        res=gd.getData(queryString)
        nextDay=datetime.datetime.now()
        if xxlx=='11':
            for data in res:
                lrjs=datetime.datetime.strptime(data[3],'%Y-%m-%d %H:%M:%S')
                jgDay=(lrjs-nextDay).days+1
                if jgDay<=gv.jsCjLrJgDay:
                    user=data[0]
                    content=title+contentTem.format(data[1],data[2],lrCjTxPara(jgDay))
                    if user and user not in gv.cjLrExcludeUser:
                        t=sendAndWrite(user, title, content)
                        sendtime = nextDay.strftime('%Y-%m-%d %H:%M:%S')
                        L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        elif xxlx=='14':#学业预警消息
            for data in res:
                user=data[0]
                content=title+contentTem.format(data[1],data[2])
                if user:
                    t=sendAndWrite(user,title,content)
                    sendtime=nextDay.strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))

        else:
            pass
    elif xxlx in ['15']:
        njZyXsxx=gd.getData(gv2.getZyxxCode)
        zfksjssj=gd.getData(gv2.getCjZfQsJsSj)
        sendtime=datetime.datetime.now()
        if (datetime.datetime.strptime(zfksjssj[0][0],'%Y-%m-%d %H:%M:%S')-sendtime).days==gv2.cjZfTxJgDay:
            for njzy in njZyXsxx:
                queryString=baseQueryString.format(njzy[0],njzy[1])
                res=gd.getData(queryString)
                for data in res:
                    user=data[0].split(',')###该处与众不同，传递的是列表
                    sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    content=contentTem.format(zfksjssj[0][0],zfksjssj[0][1])
                    #print(content)
                    t=sendAndWrite(user,title,content)
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['16']:
        zcxqj = getZcXqj(jgDay)
        if zcxqj[0] in gv.jsJxrwTtkTxZc and zcxqj[1] in gv.jsJxrwTtkTxXqj:
            queryString=baseQueryString
            res=gd.getData(queryString)
            for data in res:
                user=data[0]
                content=title+contentTem.format(data[1],data[2])
                t=sendAndWrite(user,title,content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    else:
        pass
    if L:
        gd.insertSqlite(L)#发送完成后插入数据库
    return len(L)

