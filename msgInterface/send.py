import json
import requests
import datetime
from msgPackage import gzdxVAR as gv

# ----设置account信息
accountid = gv.accountid#'gzhujwxt'
accountkey = gv.accountkey#'zpGZ5c5cku471M3741C3gdbPO0'
def sendToUser(receiver,tit,cont,type='02'):
    '''paramas:receiver:内部接收人,tit:消息标题,con:消息正文,type:消息类型'''
    nowTime = datetime.datetime.now()
    sendTime = nowTime.strftime('%Y-%m-%d %H:%M:%S')  # 发送时间
    title = tit
    # ----设置消息内容
    content = cont
    # ---设置typecode,isCron
    typecode = type
    isCron = '0'
    # 设置渠道信息
    channels = ''
    channelIds = ''
    chan = {'channels': channels, 'channelIds': channelIds}
    # 设置内、外部接收人信息
    ##测试时使用
    if isinstance(receiver,list):
        intReceiver=receiver
    else:
        intReceiver =[receiver]#['100809','103667']#[receiver]#测试时.extend(['100809','103667'])
    extReceiver = {}
    # 设置其他信息
    ext = {}
    msjon = {'title': title,
             'content': content,
             'isCron': isCron,
             'sendtime': sendTime,
             'typecode': typecode,
             'channels': channels,
             'channelIds': channelIds,
             'intReceiver': intReceiver,
             'extReceiver': extReceiver,
             'ext': ext
             }
    #print(msjon)
    account = {'accountID': accountid, 'accountKey': accountkey}
    postacc = [('accountID', accountid), ('accountKey', accountkey)]
    baseURL = 'http://172.17.1.134'
    charset = 'utf-8'
    # 获取动态获取接收端渠道列表
    getChannelsUrl = '/restful/get_channels'
    url = baseURL + getChannelsUrl
    # print(url)
    # ---解析jsonData,获取渠道信息
    #jsonData = requests.get(url, params=account).json()  # 请求建立渠道,并返回json
    #print(jsonData)
    #data = jsonData['data']['ydxy-corp'][2]  # 解析微信企业号信息
    #print(data)
    data={'status':0}
    if data['status'] == 0 or data['status'] == '0':
        postUrl = '/restful/sendmsg'
        url = baseURL + postUrl
        channels = 'ydxy-corp'  # data['channelName']
        channelIds = '8926702c-e93a-4d34-a3e7-e2dd8e3431cd'#data['id']
        chan = {'channels': channels, 'channelIds': channelIds}
        #print(chan)
        msjon.update(chan)  # 更新mjson
        msjon = json.dumps(msjon)
        #print(msjon)
        postacc.append(("msgJson", msjon))
        #t=''
        #print(postacc)
        r = requests.post(url, data=postacc,headers={'charset':charset})
        t=json.loads(r.text)
        #print(t)
        # print(t['MESSAGE'])
        return t
    else:
        print('渠道不可用')
        return ''

def LocalsendToUser(receiver,tit,cont,type='02'):
    receiver=[receiver]
    print(receiver)
    return {'MESSAGE':'CODE'}

#sendToUser('103667','tilte','content')