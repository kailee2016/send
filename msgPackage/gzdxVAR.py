##############setting the control paramars############################

############
debug=False
##########set the send time paras######################
keBiaoZc=[1]#课表发送周次['1','2','3'],教师与学生共用
keBiaoJgDay=1#课表发送提前天数
ksJgDay=2#考试发送提前天数
otherJgDay=0#其他发送提前天数,常用的有调停课，场地借用，学籍异动，缓考，
##################setting the grade commits paras##########
jsCjLrJgDay=3#提醒教师提交成绩的时间间隔,
cjLrExcludeUser=['102961']
xsCjTxSfFsCjb=1#是否向学生发送cjb中的数据，为0表示只发送补录表中的数据
####################选课提醒参数##########
xkTxNj=['2019']#选课提醒年级
xkTxZc=[18,19,20]#选课提醒周次
xkTxXqj=[2]#选课提醒星期几
xkTxRq=['2019-09-03','2019-09-04']#选课提醒日期
############setting the xxlx status###########
############慕课修读提醒参数################
xkMkTxRq=['2019-09-16']
xkMkTxZc=[]
xkMkTxXqj=[]
############教学任务停开提醒
jsJxrwTtkTxZc=[19]
jsJxrwTtkTxXqj=[1]
#######set the MsgCenter paras#############
accountid = 'gzhujwxt'
accountkey = 'zpGZ5c5cku471M3741C3gdbPO0'
####################################setting the jw database sql code##################################
###############setint the message comments######################
messageComments='''【广州大学教务处】'''
#######################################################################################################
##取日期对应的周次，星期##
getXtZcXqjSqlCode='''select zc,xqj from jw_pk_rcmxb where rq='{}' '''
#取日期对应的周次，星期对应的教师课表####
getNextDayKbCode='''select distinct jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc from LIKAI_QXKB t where bitand(t.zcd,get_jctobinary('{}'))>0 and t.xqj='{}' and 1=1'''
##取日期对应的周次，星期对应的学生课表###
getNextDayXsKbCode='''select distinct jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc,
(select xh from jw_xjgl_xsjbxxb where xh_id=xkb.xh_id) xsxh,
(select xm from jw_xjgl_xsjbxxb where xh_id=xkb.xh_id) xsxm 
from LIKAI_QXKB t,
jw_xk_xsxkb xkb
where bitand(t.zcd,get_jctobinary('{}'))>0 and t.xqj='{}' and 1=1
and xkb.xnm=(select zdz from zftal_xtgl_xtszb where zs='当前学年')
and xkb.xqm=(select zdz from zftal_xtgl_xtszb where zs='当前学期')
and xkb.jxb_id=t.jxb_id'''
##取当天办理的学籍异动信息###
######发向教师 03
getXjYdxxCode='''select (select xh from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xh,(select xm from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xm,
(select xjydmc from jw_xjgl_xjydlbdmb where ydlbm=ydb.ydlbm) ydmc,(case when to_number(ydb.shzt)=3 then '已通过' else '不通过' end) jg,
  t.jgh,t.XM
from jw_xjgl_xjydb ydb,(select jzg.jgh,jzg.xm,jzg.JG_ID
from ZFTAL_XTGL_YHJSB yh,JW_JG_JZGXXB jzg
where yh.JSDM in (
  select jsdm
  from ZFTAL_XTGL_JSXXB jsb
  where jsb.jsmc = '学院')
and yh.YHM=jzg.JGH) t where ZZSHSJ like '%{}%' and to_number(shzt)>=3 and 1=1 and ydb.YDHJG_ID=t.JG_ID'''
######学籍异动发向学生 031
getXjYdxxCode031='''select (select xh from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xh,(select xm from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xm,
(select xjydmc from jw_xjgl_xjydlbdmb where ydlbm=ydb.ydlbm) ydmc,(case when to_number(ydb.shzt)=3 then '已通过' else '不通过' end) jg
from jw_xjgl_xjydb ydb where ZZSHSJ like '%{}%' and to_number(shzt)>=3 and 1=1 '''
###################################################################
###取场地借用信息
getCdJyCode='''select distinct
  (select jgh
   from JW_JG_JZGXXB
   where JGH_ID = yub.syr_id)                        jgh,
  (select xm
   from JW_JG_JZGXXB
   where JGH_ID = yub.syr_id)                        xm,
  (select WM_CONCAT(cdb.CDMC)
   from JW_PK_JXCDYUYMXB mxb, JW_JCDM_CDXQXXB cdb
   where mxb.XNM = cdb.XNM and mxb.xqm = cdb.XQM and mxb.CD_ID = cdb.CD_ID
         and mxb.YYXX_ID = yub.YYXX_ID) || '(' ||
  (select distinct
     '第' || fn_bittozc(2 * zcd) || '周，星期' || replace(LIKAI_JW_PUBLICINTERFACE.RETURN_CDYYXQ(t.YYXX_ID), '7', '日') ||
     ',第' ||
     fn_bittozc(2 * jc) || '节)'
   from JW_PK_JXCDYUYSJB t
   where t.YYXX_ID = yub.yyxx_id)                    cdjyxx,
  decode(yub.SHZT, '3', '已通过', '4','被退回','不通过') || case when yub.SHZT ='5'
    then '(原因：' || (select SUGGESTION
                    from SP_WORK_NODE t
                    where t.W_ID = yub.YYXX_ID) || ')'
                                         else '' end shjg
from JW_PK_JXCDYUYB yub
where yub.SHZT in('3','5') and yub.SHSJ like '%{}%' and 1 = 1'''
#####################################################################
###取学生考试信息
getXsKsCode='''select xh,xm,kcmc,cdb.cdmc,ccb.KSRQ||'('||ccb.KSKSSJ||'-'||ccb.KSJSSJ||')' kssj from
  jw_kw_xsksxxb ksb,jw_xjgl_xsjbxxb xsj,JW_JXRW_JXBXXB jxb,JW_JH_KCDMB kc,JW_JCDM_CDXQXXB cdb,jw_kw_kssjb sjb,jw_kw_ksccb ccb
  where ksb.xh_id=xsj.xh_id and jxb.jxb_id=ksb.jxb_id and jxb.xnm=ksb.xnm and jxb.xqm=ksb.xqm and jxb.kch_id=kc.kch_id and ksb.xnm=cdb.xnm
  and ksb.xqm=cdb.xqm and ksb.xnm=sjb.xnm and ksb.xqm=sjb.xqm and ksb.cd_id=cdb.cd_id and ksb.sjbh_id=sjb.sjbh_id and sjb.ksccb_id=ccb.ksccb_id
  and ccb.ksrq like '%{}%' and exists(select 'x' from JW_KW_KSCXKZB where ccb.KSMCDMB_ID=ksb.KSMCDMB_ID and XSCZWH='1')
and not exists(select 'x' from JW_XMGL_JXXMXSBMQKB qtb where qtb.JXXMLBDM='1005' and SHJG='3' and qtb.XNM=ksb.XNM and qtb.XQM=ksb.XQM
and qtb.XH_ID=ksb.XH_ID and qtb.JXB_ID=ksb.JXB_ID) and 1=1'''
###################################################################
###取教师监考信息
getJsJkCode='''select distinct jzg.jgh,jzg.XM,t.kssj,cdb.cdmc,kc.KCMC, ddb.KSDD_ID,cdb.cdmc,kc.KCMC,t.kssj from JW_KW_KSDDB ddb,JW_KW_KSDDBJDZB dzb,JW_JCDM_CDXQXXB cdb,JW_JXRW_JXBXXB jxb,
  JW_JH_KCDMB kc,JW_JG_JZGXXB jzg,JW_KW_KSDDJKB jkb,(select sjb.KSMCDMB_ID,sjb.SJBH_ID,sjb.XNM,sjb.XQM,ccb.KSRQ||'('||KSKSSJ||'-'||ccb.KSJSSJ||')' kssj from JW_KW_KSSJB sjb,JW_KW_KSCCB ccb
where sjb.XNM=ccb.XNM and sjb.XQM=ccb.XQM and sjb.KSCCB_ID=ccb.KSCCB_ID and sjb.KSMCDMB_ID=ccb.KSMCDMB_ID) t
where ddb.XNM=ddb.Xnm and ddb.XQM=dzb.XQM and ddb.KSHKBJ_ID=dzb.KSHKBJ_ID
and cdb.XNM=ddb.XNM and cdb.XQM=ddb.XQM and cdb.CD_ID=ddb.CD_ID
and jxb.XNM=ddb.XNM and jxb.XQM=ddb.XQM and jxb.JXB_ID=dzb.JXB_ID and jxb.KCH_ID=kc.KCH_ID
and t.XNM=dzb.XNM and t.XQM=dzb.XQM and t.SJBH_ID=dzb.SJBH_ID
  and ddb.XNM=jkb.XNM and ddb.XQM=jkb.XQM and ddb.KSDD_ID=jkb.KSDD_ID
  and jkb.JGH_ID=jzg.JGH_ID
  and t.kssj like '%{}%'
  and exists(select 'x' from JW_KW_KSCXKZB where t.KSMCDMB_ID=KSMCDMB_ID and JSCJK='1')'''
##########################################
########调停课发送教师###############
getJsTtkCode='''select
  jzg.jgh,
  jzg.xm,
  kc.KCMC || '(教学班名称:' || jxb.JXBMC || ')'           tkxx,
  decode(ttk.SHZT, '3', '已通过', '4','被退回','不通过') || case when ttk.SHZT = '5'
    then '(原因：' || (select SUGGESTION
                    from SP_WORK_NODE t
                    where t.W_ID = ttk.TTKXX_ID) || ')'
                                         else '' end shjg
from JW_PK_TTKSQB ttk, JW_JG_JZGXXB jzg, JW_JXRW_JXBXXB jxb, JW_JH_KCDMB kc
where ttk.YJGH_ID = jzg.JGH_ID and ttk.xnm = jxb.xnm and ttk.XQM = jxb.XQM
      and ttk.JXB_ID = jxb.JXB_ID and kc.KCH_ID = jxb.KCH_ID
      and ttk.SHZT in ('3','4','5')
      and ttk.shsj like '%{}%' and ttk.XNM = (select zdz
                                                      from zftal_xtgl_xtszb
                                                      where zs = '当前学年')
      and ttk.Xqm = (select zdz
                     from zftal_xtgl_xtszb
                     where zs = '当前学期') and 1 = 1
order by ttk.yjgh_id, ttk.jxb_id, ttk.shsj'''
###########调停课发送学生################
###########
getXsTtkCode='''select distinct (select xh from jw_xjgl_xsjbxxb where xh_id=xkb.XH_ID)xh,(select xm from JW_XJGL_XSJBXXB where xh_id=xkb.XH_ID) xm,
  (select '《'||kcmc||'》课程,' from JW_JH_KCDMB where xkb.KCH_ID=kch_id)||'发生'||(case when ttk.tklxdm='02' then '补课' when
ttk.TKLXDM='03' then '停课' when ttk.YZCD||ttk.YXQJ||ttk.yjc<>ttk.XZCD||ttk.XXQJ||ttk.XJC then '上课时间变动'
else '上课地点或上课教师变动' end) kcmc
from JW_XK_XSXKB xkb,JW_PK_TTKSQB ttk
where xkb.JXB_ID=ttk.JXB_ID
and ttk.SHZT='3' and ttk.SHSJ like '%{}%'
and xkb.XNM=(select zdz from zftal_xtgl_xtszb where zs='当前学年')
and xkb.xqm=(select zdz from zftal_xtgl_xtszb where zs='当前学期')'''
#########################缓考发送学生#############
getXsHkCode='''select (select xh from JW_XJGL_XSJBXXB where xh_id=qtb.XH_ID) xh,
(select xm from JW_XJGL_XSJBXXB where xh_id=qtb.XH_ID) xm,
  '对教学班：'||(select jxbmc from JW_JXRW_JXBXXB where jxb_id=qtb.JXB_ID)||'申请的“'||(select szb.JXXMLBMC from JW_XMGL_JXXMBMSZB szb where szb.JXXMLBDM=qtb.jxxmlbdm)||'”' xmmc,
 decode(qtb.SHJG,'3','已通过','不通过') shjg
from JW_XMGL_JXXMXSBMQKB qtb where qtb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and qtb.xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期') and qtb.SHSJ like '%{}%' and qtb.SHJG>=3'''
###################学生成绩有变动(含新增),成绩表，与成绩补录表
getXscjCode='''select distinct
  t.xh,
  t.xm,
  WM_CONCAT('《'||t.kcmc || '》课程,成绩为:' || t.cj)
from (
       select
         xsj.xh   xh,
         xsj.xm   xm,
         cjb.kcmc kcmc,
         cjb.cj
       from JW_CJ_XSCJB cjb, JW_XJGL_XSJBXXB xsj
       where cjb.XH_ID = xsj.XH_ID
             and cjb.XNM = (select zdz
             from ZFTAL_XTGL_XTSZB
             where zs = '当前学年')
             and cjb.XQM = (select zdz
             from ZFTAL_XTGL_XTSZB
             where zs = '当前学期')
             and 1={}
             and cjb.CZSJ like '%{}%'
             and cjb.CJZT ='3'
       union
       select
         xsj.xh  xh,
         xsj.xm  xm,
         kc.KCMC kcmc,
         blb.CJ
       from JW_CJ_CJBLB blb, JW_XJGL_XSJBXXB xsj, JW_JH_KCDMB kc
       where blb.XH_ID = xsj.XH_ID
             and blb.KCH_ID = kc.KCH_ID
             and blb.shsj like '%{}%'
             and blb.SHZT = '3'
     ) t
group by t.xh, t.xm
'''
############教师录入成绩提醒表######################
getJsLrCjTxCode='''
select jzg.jgh,jzg.XM,jxb.JXBMC,szb.LRJSSJ
from JW_CJ_CJLRMMB mmb,JW_JG_JZGXXB jzg,JW_CJ_XMBLSZB szb,JW_JXRW_JXBXXB jxb
where mmb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='成绩录入学年')
and mmb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='成绩录入学期')
and mmb.YJXB_ID is null
and mmb.JXB_ID=jxb.JXB_ID
and mmb.JGH_ID=jzg.JGH_ID
and mmb.JXB_ID=szb.JXB_ID
and szb.LRZT in ('1','2')
and szb.lrjssj is not null
and szb.ZHYCCJXBJ='1'
'''

################系统异常检测#############################
###############考试冲突################



##############选课容量不足，座位数不足###############



##############必修课程冲突#############






#############具体年级必修课程选课提醒#########################
getNjBxKcTxCode='''
select
xh,xm,WM_CONCAT(kcmc) bxkc
from
  (select
     xsj.xh,
     xsj.xm,
    xjb.NJDM_ID,
     t.KCH_ID,
     kc.KCMC,
     xsj.XH_ID
   from
     (select distinct
        hbb.BH_ID,
        jxb.KCH_ID
      from JW_JXRW_JXBHBXXB hbb, JW_JXRW_JXBXXB jxb
      where jxb.JXB_ID = hbb.JXB_ID
            and jxb.XNM = (select zdz
                           from ZFTAL_XTGL_XTSZB
                           where zs = '选课学年')
            and jxb.xqm = (select zdz
                           from ZFTAL_XTGL_XTSZB
                           where zs = '选课学期')
            and hbb.KCXZDM in (select kcxzdm
                               from JW_JH_KCXZDMB
                               where xbx = 'bx')
      union
      select distinct
        dzb.bh_id,
        t0.kch_id
      from JW_JXRW_BKZYBJDZB dzb, JW_JXRW_BKXXB xxb, JW_JXRW_BKLXB lxb, (select
                                                                           BKLX_ID,
                                                                           KCH_ID
                                                                         from JW_JXRW_BKLXKZDZB t1, JW_JH_KZKCDMB t2
                                                                         where t1.KZ_ID = t2.KZ_ID) t0
      where dzb.BKXXB_ID = xxb.BKXXB_ID
            and xxb.BKLX_ID = lxb.BKLX_ID
            and t0.BKLX_ID = lxb.BKLX_ID
            and xxb.XNM = (select zdz
                           from ZFTAL_XTGL_XTSZB
                           where zs = '选课学年')
            and xxb.XQM = (select zdz
                           from ZFTAL_XTGL_XTSZB
                           where zs = '选课学期')) t, jw_xjgl_xsjbxxb xsj, jw_xjgl_xsxjxxb xjb, JW_JH_KCDMB kc
   where t.BH_ID = xjb.BH_ID and kc.KCH_ID = t.KCH_ID and xsj.XH_id = xjb.XH_ID and xjb.XJZTDM in (select xjztdm
                                                                                                   from JW_XJGL_XJZTDMB
                                                                                                   where SFYXJ = '1')
         and xjb.XNM = (select zdz
                        from ZFTAL_XTGL_XTSZB
                        where zs = '选课学年') and xjb.XQM = (select zdz
                                                          from ZFTAL_XTGL_XTSZB
                                                          where zs = '选课学期')) t
  where 1=1 and
 not exists(select 'x'
                 from jw_xk_xsxkb xkb
                 where xkb.xnm = (select zdz
                                  from ZFTAL_XTGL_XTSZB
                                  where zs = '选课学年') and
                       xkb.XQM = (select zdz
                                  from ZFTAL_XTGL_XTSZB
                                  where zs = '选课学期') and xkb.XH_ID = t.XH_ID and xkb.KCH_ID = t.KCH_ID)
and t.NJDM_ID like '%{}%'
group by xh,xm'''


##################取当前学年，网络视频课选课名单
getXsWlspk='''
select (select xh from JW_XJGL_XSJBXXB where xh_id=xkb.xh_id) xh,
  (select xm from JW_XJGL_XSJBXXB where xkb.XH_ID=XH_ID) xm,
  kc.kcmc,
  kc.bz
from jw_jh_kcdmb kc,JW_XK_XSXKB xkb
where (kc.bz like '%开课平台%' or kc.bz like '%上课网址%')
and xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期')
and xkb.KCH_ID=kc.KCH_ID
and kc.kcmc not like '%军事%训练%'
'''


###################取当前学年学期预警的学生名单
#######思路先发送当天处理的，并将当天发送的数据存入备份表likai_yesterdat_xyyjclb
getXsXyYjCode='''
select
  xsj.XH,
  xsj.xm,
  '截至当前，您共获学分为：' || jgb.TJTJZ || ',不足' || xsj.njdm_id || '级' || (select zymc
                                                                 from ZFTAL_XTGL_ZYDMB
                                                                 where xsj.ZYH_ID = zyh_id) || '专业学分要求的3/4(' ||
  tjb.SXZ || '学分)，已被给予学业预警,您共被预警' || (select count(*)
                                      from JW_CJ_XYYJCLJGB
                                      where jgb.CLZT = '1' and xh_id = jgb.xh_id) || '次。' || case when (select count(*)
                                                                                                        from
                                                                                                          JW_CJ_XYYJCLJGB
                                                                                                        where
                                                                                                          jgb.CLZT = '1'
                                                                                                          and xh_id =
                                                                                                              jgb.xh_id)
                                                                                                       > 1
    then '请您尽快办理“延长在读年限”异动！'
                                                                                             else '希望您牟足劲,补齐所缺学分!' end yjnr
from JW_CJ_XYYJJGB jgb, JW_XJGL_XSJBXXB xsj, JW_CJ_XYYJTJB tjb, JW_CJ_XYYJCLJGB clb
where jgb.XH_ID = xsj.XH_ID
      and jgb.XH_ID = clb.XH_ID
      and jgb.XYYJTJ_ID = tjb.XYYJTJ_ID
      and clb.XNM = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '当前学年')
      and clb.xqm = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '当前学期')
      and clb.XYYJJG_ID = jgb.XYYJJG_ID
and not exists(select 'x' from likai_yesterdat_xyyjclb where xnm=clb.XNM and xqm=clb.XQM and xh_id=clb.XH_ID )
'''
############取教师停开教学任务信息
getJsTkKcxx='''
select
  (select jgh
   from jw_jg_jzgxxb
   where rkb.JGH_ID = jgh_id) jgh,
  (select xm
   from JW_JG_JZGXXB
   where rkb.JGH_ID = jgh_id) xm,
  '课程《'||(select KCMC
   from JW_JH_KCDMB
   where jxb.KCH_ID = kch_id) || '》（教学班名称：' || jxb.JXBMC || ',选课人数：'||(select count(*)
                                                            from JW_XK_XSXKSXB sxb
                                                            where sxb.JXB_ID = jxb.jxb_id) || '),已经被停开，详情与开课学院或教务科联系！' content
from JW_JXRW_JXBXXB jxb, JW_JXRW_JXBJSRKB rkb
where jxb.XNM = (select zdz
                 from ZFTAL_XTGL_XTSZB
                 where zs = '选课学年')
      and jxb.xqm = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '选课学期')
      and jxb.JXB_ID = rkb.JXB_ID
and jxb.KKZT='4'
'''